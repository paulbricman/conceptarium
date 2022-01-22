import streamlit as st
import requests
import json


def paint():
    with st.sidebar:
        with st.expander('🔌 connected microverses', expanded=True):
            microverses = st.session_state.get('microverses', [])

            if len(microverses) > 0:
                for e_idx, e in enumerate(microverses):
                    if e['auth']['custodian']:
                        display_text = '🗝️ ' + e['url']
                    else:
                        display_text = e['url']
                    st.code(display_text)

                    if st.button('remove', key=(e, e_idx)):
                        st.session_state['microverses'] = st.session_state.get(
                            'microverses', [])
                        st.session_state['microverses'].remove(e)
                        st.experimental_rerun()

        with st.expander('🆕 connect to new microverse', expanded=True):
            url = st.text_input('conceptarium url',
                                key=st.session_state.get('microverses', []))
            token = st.text_input(
                'access token', key=st.session_state.get('microverses', []))

            if st.button('add'):
                if '://' not in url:
                    url = 'http://' + url
                if url[-1] == '/':
                    url = url[:-1]
                if url[-5:] != ':8000':
                    url += ':8000'
                custodian_check = json.loads(
                    requests.get(url + '/custodian/check', params={
                        'token': token
                    }).content)

                st.session_state['microverses'] = st.session_state.get(
                    'microverses', []) + [{
                        'url': url,
                        'token': token,
                        'auth': custodian_check
                    }]

                st.experimental_rerun()

        with st.expander('🗝️ shared microverses', expanded=True):
            custodian_microverse = [
                e for e in st.session_state.get('microverses', []) if e['auth']['custodian'] == True]
            if len(custodian_microverse) > 0:
                shared_microverses = json.loads(requests.get(custodian_microverse[0]['url'] + '/microverse/list', params={
                    'token': custodian_microverse[0]['token']
                }).content)
                for e_idx, e in enumerate(shared_microverses):
                    st.code(e['token'])

                    if st.button('remove'):
                        requests.get(custodian_microverse[0]['url'] + '/microverse/remove', params={
                            'token': custodian_microverse[0]['token'],
                            'microverse': e['token']
                        })
                        st.info(
                            'The microverse has been removed.')
                        st.experimental_rerun()
