import streamlit as st
from streamlit.uploaded_file_manager import UploadedFile
import requests
import json
import io
from PIL import Image


def load(modality, query):
    thoughts = []
    query_embeddings = None

    for microverse in st.session_state.get('microverses', []):
        url = microverse['url']
        url += '/find'

        if modality == 'text':
            response = requests.get(url, params={
                'token': microverse['token'],
                'query': query,
                'relatedness': st.session_state['ranker_relatedness'],
                'activation': st.session_state['ranker_activation'],
                'noise': st.session_state['ranker_noise'],
                'return_embeddings': False
            })
        elif modality == 'image':
            if isinstance(query, UploadedFile):
                query = Image.open(io.BytesIO(query.getvalue()))

            img_io = io.BytesIO()
            query = query.convert('RGB')
            query.save(img_io, 'jpeg')
            img_io.seek(0)
            query = img_io.read()

            response = requests.post(url, data={
                'token': microverse['token'],
                'relatedness': st.session_state['ranker_relatedness'],
                'activation': st.session_state['ranker_activation'],
                'noise': st.session_state['ranker_noise'],
                'return_embeddings': False
            }, files={
                'query': query})

        content = json.loads(response.content)
        new_thoughts = content['authorized_thoughts']
        for e_idx, e in enumerate(new_thoughts):
            new_thoughts[e_idx]['conceptarium_url'] = microverse['url']
            new_thoughts[e_idx]['access_token'] = microverse['token']
            new_thoughts[e_idx]['auth'] = microverse['auth']

        if isinstance(content, dict):
            thoughts += content['authorized_thoughts']

    return thoughts
