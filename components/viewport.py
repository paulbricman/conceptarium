import streamlit as st
import pickle
from sentence_transformers import util
import torch
import numpy as np
import time


def get_name():
    return '🪟 viewport'


@st.cache(persist=True, allow_output_mutation=True)
def load_thoughts():
    thoughts = pickle.load(open('conceptarium/metadata.pickle', 'rb'))
    langauge_centroid = torch.mean(torch.stack([e.embedding for e in thoughts if e.modality == 'language']), -2)
    imagery_centroid = torch.mean(torch.stack([e.embedding for e in thoughts if e.modality == 'imagery']), -2)
    
    print(imagery_centroid - langauge_centroid)

    for thought_idx, thought in enumerate(thoughts):
        if thought.modality == 'imagery':
            thoughts[thought_idx].embedding += langauge_centroid - imagery_centroid
    
    return thoughts

    
def paint(cols):
    if st.session_state.get('navigator_embedding', None) is not None:
        thoughts = load_thoughts()
        results = util.semantic_search(
            [st.session_state['navigator_embedding']],
            [e.embedding for e in thoughts], top_k=50)
        results = [e for e in results[0] if e['score'] > 0.7]

        for result_idx, result in enumerate(results):
            results[result_idx]['score'] = (st.session_state['ranker_relatedness'] * result['score']
                                    + st.session_state['ranker_activation'] *
                                    (np.log(thoughts[result['corpus_id']].interest / (1 - 0.9)) - 0.9 * np.log((time.time() - thoughts[result['corpus_id']].timestamp) / (3600 * 24) + 0.1))) \
                * np.random.normal(1, st.session_state['ranker_noise'])

        results = sorted(results, key=lambda result: result['score'], reverse=True)

        if thoughts[results[0]['corpus_id']].get_content() == st.session_state['navigator_input']:
            results = results[1:]

        for result_idx, result in enumerate(results):
            with cols[result_idx % len(cols)]:
                thought = thoughts[result['corpus_id']]
                if thought.modality == 'language':
                    st.success(thought.get_content())
                elif thought.modality == 'imagery':
                    st.image(thought.get_content())

                if st.button('jump', thought):
                    st.session_state['navigator_input'] = thought.get_content()
                    st.session_state['navigator_modality'] = thought.modality
                    st.session_state['navigator_embedding'] = thought.embedding
                    st.experimental_rerun()

    