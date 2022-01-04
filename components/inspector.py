import streamlit as st
import pickle
from sentence_transformers import util
from datetime import datetime


def get_name():
    return '🔍 inspector'


@st.cache(persist=True, allow_output_mutation=True)
def load_thoughts():
    return pickle.load(open('conceptarium/metadata.pickle', 'rb'))


def paint():
    if st.session_state.get('navigator_embedding', None) is not None:
        thoughts = load_thoughts()
        results = util.semantic_search(
            [st.session_state['navigator_embedding']],
            [e.embedding for e in thoughts])

        if results[0][0]['score'] > 0.98:
            thought = thoughts[results[0][0]['corpus_id']]
            st.markdown('**modality**: ' + thought.modality)
            st.markdown('**filename**: ' + thought.filename.split('/')[-1])
            st.markdown('**timestamp**: ' + datetime.utcfromtimestamp(int(thought.timestamp)).strftime("%d.%m.%Y"))
            st.markdown('**interest**: ' + str(thought.interest))
            
        else:
            st.caption('No thought within reach.')

    