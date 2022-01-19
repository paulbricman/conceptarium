import streamlit as st
import requests
import json
import io


def load(modality, query):
    thoughts = []
    query_embeddings = None

    for microverse in st.session_state.get('microverses', []):
        url = microverse['url']

        if url[-1] != '/':
            url += '/'
        url += 'find'

        if modality == 'text':
            response = requests.get(url, params={
                'token': microverse['token'],
                'query': query
            })
        elif modality == 'image':
            response = requests.post(url, data={
                'token': microverse['token']}, files={
                'query': query
            })

        content = json.loads(response.content)

        if isinstance(content, dict):
            thoughts += content['authorized_thoughts']
            query_embeddings = content['query_embeddings']

    return query_embeddings, thoughts
