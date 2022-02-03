import requests
import streamlit as st
import numpy as np
from PIL import Image
import io
from . import knowledge


def get_name():
    return '🪟 viewport'


def paint(cols):
    if st.session_state.get('authorized_thoughts', None) is not None:
        authorized_thoughts = st.session_state['authorized_thoughts']
        similarity_threshold = 0.3
        authorized_thoughts = [
            e for e in authorized_thoughts if e['relatedness'] > similarity_threshold]

        for e_idx, e in enumerate(authorized_thoughts):
            with cols[e_idx % len(cols)]:
                if e['modality'] == 'text':
                    st.success(e['content'])
                elif e['modality'] == 'image':
                    url = e['conceptarium_url'] + '/static?token=' + e['access_token'] + '&filename=' + \
                        e['content']

                    response = requests.get(url)
                    image = Image.open(io.BytesIO(response.content))
                    st.image(image)

                if st.button('jump (' + str(round(e['relatedness'], 2)) + ')', e['content'], help='Use this as the basis of a new search query.'):
                    st.session_state['navigator_input'] = e['content']
                    st.session_state['navigator_modality'] = e['modality']
                    st.session_state['authorized_thoughts'] = knowledge.load(
                        e['modality'], e['content'])
                    st.experimental_rerun()
