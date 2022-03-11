import datetime
import streamlit as st
import requests
import json
import extra_streamlit_components as stx
from time import sleep
import os
from pathlib import Path
import random


def paint():
    cookie_manager = get_cookie_manager()
    user_state = cookie_manager.get('user_state')

    if not user_state:
        sleep(1.)
        user_state = cookie_manager.get('user_state')
        if not user_state:
            user_state = {}

    user_state['layout'] = user_state.get('layout', default_layout())
    user_state['microverses'] = user_state.get('microverses', [])
    st.session_state['microverses'] = user_state['microverses']
    st.session_state['layout'] = user_state['layout']

    with st.sidebar:
        with st.expander('🗔 layout', expanded=True):
            user_state['layout']['viewportCols'] = int(st.number_input(
                'viewport cols', 1, 5, user_state['layout'].get('viewportCols', 3), 1))

            faux_components = ['header', 'knowledge',
                               'microverses', 'viewport']

            components_path = Path('components')
            if not components_path.exists():
                components_path = Path('frontend') / 'components'

            components = [e.split('.')[0] for e in os.listdir(components_path) if e.endswith(
                '.py') and e.split('.')[0] not in faux_components]
            user_state['layout']['leftColumn'] = st.multiselect(
                'left column', components, user_state['layout'].get('leftColumn', ['navigator', 'ranker']))
            user_state['layout']['rightColumn'] = st.multiselect(
                'right column', components, user_state['layout'].get('rightColumn', ['inspector']))
            st.session_state['layout'] = user_state['layout']
            cookie_manager.set('user_state', user_state, expires_at=datetime.datetime.now(
            ) + datetime.timedelta(days=30))

        if len(user_state['microverses']) > 0:
            with st.expander('🔌 connected microverses', expanded=True):
                for e_idx, e in enumerate(user_state['microverses']):
                    if e['auth']['custodian']:
                        display_text = '🗝️ ' + e['url']
                    else:
                        display_text = e['url']
                    st.code(display_text)

                    if e['auth']['custodian']:
                        if st.button('create archive'):
                            archive = requests.get(e['url'] + '/dump',
                                                   headers={'Authorization': f"Bearer {e['token']}"}).content
                            st.download_button(
                                'download archive', data=archive, file_name='knowledge.zip')

                    if st.button('remove', key=(e, e_idx), help='Remove this source of thoughts.'):
                        user_state['microverses'].remove(e)
                        cookie_manager.delete('user_state')
                        cookie_manager.set(
                            'user_state', user_state, expires_at=datetime.datetime.now() + datetime.timedelta(days=30), key='remove')
                        sleep(0.5)

        with st.expander('🆕 connect to new microverse', expanded=True):
            url = st.text_input('conceptarium url',
                                key=user_state['microverses'], help='Specify the base URL of the conceptarium you wish to access thoughts from. If you\'re trying to connect to your local instance, enter `localhost`.')
            token = st.text_input(
                'access token', key=user_state['microverses'], help='Specify the token to be used in authorizing access to this conceptarium. If you\'re the custodian of this conceptarium, enter your custodian token. If this is someone else\'s instance, please use the microverse token they provided you with.', type='password')

            if st.button('add', help='Add this conceptarium as a source of thoughts to be explored.'):
                if '://' not in url:
                    url = 'http://' + url
                if url[-1] == '/':
                    url = url[:-1]

                custodian_check = json.loads(
                    requests.get(url + '/custodian/check',
                                 headers={'Authorization': f"Bearer {token}"}).content)
                if len([e for e in user_state['microverses'] if e['url'] == url]) == 0:
                    user_state['microverses'] += [{
                        'url': url,
                        'token': token,
                        'auth': custodian_check
                    }]
                cookie_manager.set(
                    'user_state', user_state, expires_at=datetime.datetime.now() + datetime.timedelta(days=30), key='add')
                sleep(0.5)
                st.session_state['microverses'] = user_state['microverses']

        custodian_microverse = [
            e for e in user_state['microverses'] if e['auth']['custodian'] == True]
        if len(custodian_microverse) > 0:
            shared_microverses = json.loads(requests.get(custodian_microverse[0]['url'] + '/microverse/list',
                                                         headers={'Authorization': f"Bearer {custodian_microverse[0]['token']}"}).content)
            if len(shared_microverses) > 0:
                with st.expander('🗝️ shared microverses', expanded=True):
                    for e_idx, e in enumerate(shared_microverses):
                        if isinstance(e, dict):
                            st.code(e['token'])
                            if e['modality'] == 'text':
                                st.success(e['content'])

                            if st.button('disable', help='Disable the access to this microverse.'):
                                requests.get(custodian_microverse[0]['url'] + '/microverse/remove', params={
                                    'microverse': e['token']
                                }, headers={'Authorization': f"Bearer {custodian_microverse[0]['token']}"})
                                st.info(
                                    'The microverse has been removed.')
                                st.experimental_rerun()


def default_layout():
    return {
        'viewportCols': 3,
        'leftColumn': ['navigator', 'ranker'],
        'rightColumn': ['inspector']
    }


@st.cache(allow_output_mutation=True)
def get_cookie_manager():
    return stx.CookieManager()
