import streamlit as st
import pickle
from datetime import datetime
import numpy as np
import time


def get_name():
    return '🔍 inspector'


@st.cache(persist=True, allow_output_mutation=True)
def load_thoughts():
    return pickle.load(open('conceptarium/metadata.pickle', 'rb'))


def paint():
    if st.session_state.get('navigator_embedding', None) is not None:
        thoughts = load_thoughts()
        match = [e for e in thoughts if e.get_content() == st.session_state['navigator_input']]

        if len(match) > 0:
            thought = match[0]
            st.markdown('**type**: past entry')
            if thought.modality == 'language':
                st.success(thought.get_content())
            elif thought.modality == 'imagery':
                st.image(thought.get_content())

            st.markdown('**modality**: ' + thought.modality)
            st.markdown('**filename**: ' + thought.filename.split('/')[-1])
            st.markdown('**timestamp**: ' + datetime.utcfromtimestamp(int(thought.timestamp)).strftime("%d.%m.%Y"))
            st.markdown('**interest**: ' + str(round(np.log(thought.interest / (1 - 0.9)) - 0.9 * np.log((time.time() - thought.timestamp) / (3600 * 24) + 0.1), 2)))
        else:
            st.markdown('**type**: custom query')
            if st.session_state['navigator_modality'] == 'language':
                st.success(st.session_state['navigator_input'])
            elif st.session_state['navigator_modality'] == 'imagery':
                st.image(st.session_state['navigator_input'])

    