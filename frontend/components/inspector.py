import streamlit as st
from streamlit.uploaded_file_manager import UploadedFile
from datetime import datetime
import numpy as np
import time
import requests
import json
from PIL import Image
import io
from . import knowledge


def paint():
    if st.session_state.get('authorized_thoughts', None) is not None:
        thoughts = st.session_state['authorized_thoughts']

        match = [
            e for e in thoughts if st.session_state['navigator_input'] == e['content']]

        if len(match) > 0:
            thought = match[0]
            st.markdown('**type**: past entry')
            if thought['modality'] == 'text':
                st.success(thought['content'])
            elif thought['modality'] == 'image':
                url = thought['conceptarium_url'] + '/static?filename=' + \
                    thought['content']
                image = knowledge.fetch_image(url, thought['access_token'])
                st.image(image)

            st.markdown('**modality**: ' + thought['modality'])
            st.markdown('**timestamp**: ' + datetime.utcfromtimestamp(
                int(thought['timestamp'])).strftime("%d.%m.%Y"))
            st.markdown('**interest**: ' + str(round(thought['interest'], 2)))
            st.markdown('**activation**: ' + str(round(np.log(thought['interest'] / (1 - 0.9)) -
                        0.9 * np.log((time.time() - thought['timestamp']) / (3600 * 24) + 0.1), 2)))
            st.markdown('**custodian**: ' + str(thought['auth']['custodian']))
            st.markdown('**conceptarium**: ' + thought['conceptarium_url'])

            if thought['auth']['custodian']:
                if st.button('remove', help='Delete this thought from your conceptarium. Only available for custodians.'):
                    requests.get(thought['conceptarium_url'] + '/remove', params={
                        'filename': thought['filename']
                    }, headers={'Authorization': f"Bearer {thought['access_token']}"})
                    st.info(
                        'The thought has been removed, which should be reflected in future navigator jumps.')
        else:
            st.markdown('**type**: custom query')
            if st.session_state['navigator_modality'] == 'text':
                st.success(st.session_state['navigator_input'])
            elif st.session_state['navigator_modality'] == 'image':
                st.image(st.session_state['navigator_input'])

            custodian_microverse = [
                e for e in st.session_state['microverses'] if e['auth']['custodian'] == True]
            if len(custodian_microverse) > 0:
                if st.button('save', help='Persist this content as a new thought in your conceptarium. Only available for custodians.'):
                    if st.session_state['navigator_modality'] == 'text':
                        requests.get(custodian_microverse[0]['url'] + '/save', params={
                            'query': st.session_state['navigator_input']
                        }, headers={'Authorization': f"Bearer {custodian_microverse[0]['token']}"})
                    elif st.session_state['navigator_modality'] == 'image':
                        query = st.session_state['navigator_input']
                        if isinstance(query, UploadedFile):
                            query = Image.open(io.BytesIO(query.getvalue()))

                        img_io = io.BytesIO()
                        query = query.convert('RGB')
                        query.save(img_io, 'jpeg')
                        img_io.seek(0)
                        query = img_io.read()

                        requests.post(custodian_microverse[0]['url'] + '/save', files={'query': query},
                                      headers={'Authorization': f"Bearer {custodian_microverse[0]['token']}"})
                    st.info(
                        'The thought has been saved, which should be reflected in future navigator jumps.')
                if st.button('share microverse', help='Grant access to the past and future search results of this query through a microverse token.'):
                    if st.session_state['navigator_modality'] == 'text':
                        response = requests.get(custodian_microverse[0]['url'] + '/microverse/create', params={
                            'query': st.session_state['navigator_input']
                        }, headers={'Authorization': f"Bearer {custodian_microverse[0]['token']}"})
                    elif st.session_state['navigator_modality'] == 'image':
                        query = st.session_state['navigator_input']
                        if isinstance(query, UploadedFile):
                            query = Image.open(io.BytesIO(query.getvalue()))

                        img_io = io.BytesIO()
                        query = query.convert('RGB')
                        query.save(img_io, 'jpeg')
                        img_io.seek(0)
                        query = img_io.read()

                        response = requests.post(custodian_microverse[0]['url'] + '/microverse/create', files={'query': query},
                                                 headers={'Authorization': f"Bearer {custodian_microverse[0]['token']}"})

                    response = json.loads(response.content)['token']
                    st.info(response)
                    st.experimental_rerun()
