import streamlit as st
import requests
from arxiv2bib import Cli


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
                events[e_idx]['doi'] = e['name']
            if 'arxiv' in e['name']:
                if 'abs' in e['name']:
                    events[e_idx]['arxiv_id'] = e['name'].split(
                        'abs')[-1].replace('/', '')
                elif 'pdf' in e['name']:
                    events[e_idx]['arxiv_id'] = e['name'].split(
                        '/pdf/')[-1].replace('/', '').replace('.pdf', '')

        min_one_paper = False
        for e in events:
            if 'doi' in e.keys() or 'arxiv_id' in e.keys():
                st.markdown('- ' + e['name'] + ' ☑️')
                min_one_paper = True
            else:
                st.markdown('- ' + e['name'])

        if min_one_paper:
            st.markdown('')
            if st.button('show bibtex'):
                compiled_bibtex = ''
                for e in events:
                    if 'doi' in e.keys():
                        compiled_bibtex += doi_to_bibtex(e['doi']) + '\n\n'
                    elif 'arxiv_id' in e.keys():
                        compiled_bibtex += arxiv_to_bibtex(
                            e['arxiv_id']) + '\n\n'

                st.code(compiled_bibtex)
        elif events != []:
            st.markdown('')


def doi_to_bibtex(doi):
    response = requests.get('http://dx.doi.org/' + doi, headers={
        'Accept': 'application/x-bibtex'
    })
    if response.status_code == 200:
        return response.content.decode('utf-8')


def arxiv_to_bibtex(arxiv_id):
    cli = Cli([arxiv_id])
    cli.run()
    return cli.output[0]
