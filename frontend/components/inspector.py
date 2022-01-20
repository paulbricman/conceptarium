import streamlit as st
from . import knowledge
from datetime import datetime
import numpy as np
import time


def get_name():
    return '🔍 inspector'


def paint():
    if st.session_state.get('navigator_query_embeddings', None) is not None:
        thoughts = st.session_state['authorized_thoughts']

        match = [
            e for e in thoughts if st.session_state['navigator_input'] == e['content']]

        if len(match) > 0:
            thought = match[0]
            st.markdown('**type**: past entry')
            if thought['modality'] == 'text':
                st.success(thought['content'])
            elif thought['modality'] == 'image':
                url = thought['conceptarium_url'] + '/static?token=' + thought['access_token'] + '&filename=' + \
                    thought['content']
                st.image(url)

            st.markdown('**modality**: ' + thought['modality'])
            st.markdown('**timestamp**: ' + datetime.utcfromtimestamp(
                int(thought['timestamp'])).strftime("%d.%m.%Y"))
            st.markdown('**interest**: ' + str(round(thought['interest'], 2)))
            st.markdown('**activation**: ' + str(round(np.log(thought['interest'] / (1 - 0.9)) -
                        0.9 * np.log((time.time() - thought['timestamp']) / (3600 * 24) + 0.1), 2)))
            st.markdown('**custodian**: ' + str(thought['auth']['custodian']))
            st.markdown('**conceptarium**: ' + thought['conceptarium_url'])

            if thought['auth']['custodian']:
                if st.button('remove'):
                    st.error('Not implemented yet.')
        else:
            st.markdown('**type**: custom query')
            if st.session_state['navigator_modality'] == 'text':
                st.success(st.session_state['navigator_input'])
            elif st.session_state['navigator_modality'] == 'image':
                st.image(st.session_state['navigator_input'])
