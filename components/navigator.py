import streamlit as st
from sentence_transformers import SentenceTransformer
import io
from PIL import Image
import pickle
import torch


def get_name():
    return '🧭 navigator'


@st.cache(allow_output_mutation=True)
def load_model():
    return SentenceTransformer('clip-ViT-B-32')


@st.cache(persist=True, allow_output_mutation=True)
def load_imagery_shift():
    thoughts = pickle.load(open('conceptarium/metadata.pickle', 'rb'))
    langauge_centroid = torch.mean(torch.stack([e.embedding for e in thoughts if e.modality == 'language']), -2)
    imagery_centroid = torch.mean(torch.stack([e.embedding for e in thoughts if e.modality == 'imagery']), -2)
    
    return langauge_centroid - imagery_centroid


def paint():
    model = load_model()
    modality = st.selectbox('modality', ['language', 'imagery'],
        ['language', 'imagery'].index(st.session_state.get('navigator_modality', 'language')))
    embedding = None

    if modality == 'language':
        if st.session_state.get('navigator_modality', None) == 'language':
            value = st.session_state.get('navigator_input', '')
        else:
            value = ''

        input = st.text_area('input', value=value, height=300)
        embedding = model.encode(input, convert_to_tensor=True, normalize_embeddings=True)
    elif modality == 'imagery':
        if st.session_state.get('navigator_modality', None) == 'imagery':
            value = st.session_state['navigator_input']
        else:
            value = None

        input = st.file_uploader('input')
        
        if input is not None:
            embedding = model.encode(Image.open(io.BytesIO(input.getvalue())), convert_to_tensor=True, normalize_embeddings=True) + load_imagery_shift()
        elif value is not None:
            embedding = st.session_state['navigator_embedding']

    if st.button('jump'):
        st.session_state['navigator_modality'] = modality
        st.session_state['navigator_embedding'] = embedding
        st.session_state['navigator_input'] = input
        st.experimental_rerun()
    