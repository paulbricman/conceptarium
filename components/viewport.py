import streamlit as st
import pickle
from sentence_transformers import util


def get_name():
    return '🪟 viewport'


@st.cache(persist=True, allow_output_mutation=True)
def load_thoughts():
    return pickle.load(open('conceptarium/metadata.pickle', 'rb'))


def paint():
    if st.session_state.get('navigator_embedding', None) is not None:
        thoughts = load_thoughts()
        results = util.semantic_search(
            [st.session_state['navigator_embedding']],
            [e.embedding for e in thoughts])

        for result in results[0]:
            thought = thoughts[result['corpus_id']]
            if thought.modality == 'language':
                content = open(thought.filename).read()
                st.success(content)
            elif thought.modality == 'imagery':
                content = open(thought.filename, 'rb').read()
                st.image(content)

            if st.button('jump', thought):
                st.session_state['navigator_input'] = content
                st.session_state['navigator_modality'] = thought.modality
                st.session_state['navigator_embedding'] = thought.embedding
                st.experimental_rerun()

    