import streamlit as st
from . import knowledge
from datetime import datetime
import numpy as np
import time


def get_name():
    return '🔍 inspector'


def paint():
    if st.session_state.get('navigator_embedding', None) is not None:
        thoughts = knowledge.load()

        match = [
            e for e in thoughts if st.session_state['navigator_input'] == e.get_content()]

        if len(match) > 0:
            thought = match[0]
            st.markdown('**type**: past entry')
            if thought.modality == 'language':
                st.success(thought.get_content())
            elif thought.modality == 'imagery':
                st.image(thought.get_content())

            st.markdown('**modality**: ' + thought.modality)
            st.markdown('**filename**: ' + thought.filename.split('/')[-1])
            st.markdown('**timestamp**: ' + datetime.utcfromtimestamp(
                int(thought.timestamp)).strftime("%d.%m.%Y"))
            st.markdown('**activation**: ' + str(round(np.log(thought.interest / (1 - 0.9)) -
                        0.9 * np.log((time.time() - thought.timestamp) / (3600 * 24) + 0.1), 2)))
        else:
            st.markdown('**type**: custom query')
            if st.session_state['navigator_modality'] == 'language':
                st.success(st.session_state['navigator_input'])
            elif st.session_state['navigator_modality'] == 'imagery':
                st.image(st.session_state['navigator_input'])
