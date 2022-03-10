import streamlit as st
import requests


def paint():
    if st.session_state.get('authorized_thoughts') is not None:
        thought = st.session_state.get('navigator_thought')

        if thought:
            events = [thought.get('events', [])]
        else:
            events = [e.get('events', [])
                      for e in st.session_state['authorized_thoughts'] if e['relatedness'] > 0.5]

        events = [f for e in events for f in e]
        events = list({e['name']: e for e in events}.values())

        for e_idx, e in enumerate(events):
            if 'doi' in e['name']:
                events[e_idx]['bibtex'] = doi_to_bibtex(e['name'])

        compiled_bibtex = ''
        for e in events:
            if 'bibtex' in e.keys() and e['bibtex']:
                compiled_bibtex += e['bibtex'] + '\n\n'
                st.markdown('- ' + e['name'] + ' ☑️')
            else:
                st.markdown('- ' + e['name'])

        if compiled_bibtex != '':
            st.markdown('')
            if st.button('show bibtex'):
                st.code(compiled_bibtex.strip())
        else:
            st.markdown('')


def doi_to_bibtex(doi):
    response = requests.get('http://dx.doi.org/' + doi, headers={
        'Accept': 'application/x-bibtex'
    })
    if response.status_code == 200:
        return response.content.decode('utf-8')
