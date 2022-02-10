import streamlit as st
from streamlit.uploaded_file_manager import UploadedFile
import requests
import json
import io
from PIL import Image


def load(modality, query):
    thoughts = []

    for microverse in st.session_state.get('microverses', []):
        url = microverse['url']
        url += '/find'

        if modality == 'text':
            response = requests.get(url, params={
                'query': query,
                'relatedness': st.session_state['ranker_relatedness'],
                'activation': st.session_state['ranker_activation'],
                'noise': st.session_state['ranker_noise'],
                'return_embeddings': False
            }, headers={'Authorization': f"Bearer {microverse['token']}"})
        elif modality == 'image':
            if isinstance(query, UploadedFile):
                query = Image.open(io.BytesIO(query.getvalue()))

            img_io = io.BytesIO()
            query = query.convert('RGB')
            query.save(img_io, 'jpeg')
            img_io.seek(0)
            query = img_io.read()

            response = requests.post(url, data={
                'relatedness': st.session_state['ranker_relatedness'],
                'activation': st.session_state['ranker_activation'],
                'noise': st.session_state['ranker_noise'],
                'return_embeddings': False
            }, files={'query': query}, headers={'Authorization': f"Bearer {microverse['token']}"})

        content = json.loads(response.content)
        new_thoughts = content['authorized_thoughts']
        for e_idx, e in enumerate(new_thoughts):
            new_thoughts[e_idx]['conceptarium_url'] = microverse['url']
            new_thoughts[e_idx]['access_token'] = microverse['token']
            new_thoughts[e_idx]['auth'] = microverse['auth']

        if isinstance(content, dict):
            thoughts += content['authorized_thoughts']

    return thoughts


@ st.cache()
def fetch_image(url, token):
    response = requests.get(url, headers={'Authorization': f"Bearer {token}"})
    image = Image.open(io.BytesIO(response.content))
    return image
