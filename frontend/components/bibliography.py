import streamlit as st


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

        for event in events:
            st.markdown('- ' + event['name'])

        if events != []:
            st.markdown('')
