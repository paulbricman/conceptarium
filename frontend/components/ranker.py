import streamlit as st


def get_name():
    return '🏆 ranker'


def paint():
    st.session_state['ranker_relatedness'] = st.slider(
        'relatedness', -1., 1., 0.8, 0.01, help='Specify the weight of semantic similarity of thoughts to the query in ranking the search results.')
    st.session_state['ranker_activation'] = st.slider(
        'activation', -1., 1., 0., 0.01, help='Specify the weight of thought activation in ranking the search results.')
    st.session_state['ranker_noise'] = st.slider(
        'noise', 0., 0.1, 0.01, 0.001, help='Specify the desired amount of randomness in ranking the search results.')
