import streamlit as st
from . import knowledge
from sentence_transformers import util
import torch
import numpy as np
import time
import numpy as np
from numpy.linalg import norm


def get_name():
    return '🪟 viewport'


def paint(cols):
    if st.session_state.get('navigator_query_embeddings', None) is not None:
        authorized_thoughts = st.session_state['authorized_thoughts']
        query_embeddings = st.session_state['navigator_query_embeddings']
        modality = st.session_state['navigator_modality']
        relatedness = st.session_state['ranker_relatedness']
        activation = st.session_state['ranker_activation']
        noise = st.session_state['ranker_noise']

        for e in authorized_thoughts:
            if modality == 'text':
                if e['modality'] == 'text':
                    sim = np.dot(e['embeddings']['text'], query_embeddings['text']) / (
                        norm(e['embeddings']['text']) * norm(query_embeddings['text']))
                elif e['modality'] == 'image':
                    sim = np.dot(e['embeddings']['text_image'], query_embeddings['text_image']) / (
                        norm(e['embeddings']['text_image']) * norm(query_embeddings['text_image']))
            elif modality == 'image':
                sim = np.dot(e['embeddings']['text_image'], query_embeddings['text_image']) / (
                    norm(e['embeddings']['text_image']) * norm(query_embeddings['text_image']))
            e['relatedness'] = sim

        for e_idx, e in enumerate(authorized_thoughts):
            score = relatedness * e['relatedness']
            score += activation * (np.log(e['interest'] / (1 - 0.9)) - 0.9 * np.log(
                (time.time() - e['timestamp']) / (3600 * 24) + 0.1))
            score *= np.random.normal(1, noise)
            authorized_thoughts[e_idx]['score'] = score

        similarity_threshold = 0.25
        authorized_thoughts = [
            e for e in authorized_thoughts if e['relatedness'] > similarity_threshold]
        authorized_thoughts = sorted(
            authorized_thoughts, key=lambda x: x['score'], reverse=True)

        for e_idx, e in enumerate(authorized_thoughts):
            with cols[e_idx % len(cols)]:
                if e['modality'] == 'text':
                    st.success(e['content'])
                elif e['modality'] == 'image':
                    url = e['conceptarium_url'] + '/static?token=' + e['access_token'] + '&filename=' + \
                        e['content']
                    st.image(url)

                if st.button('jump', e['content']):
                    st.session_state['navigator_input'] = e['content']
                    st.session_state['navigator_modality'] = e['modality']
                    st.session_state['navigator_query_embeddings'] = e['embeddings']
                    st.experimental_rerun()
