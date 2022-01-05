import streamlit as st


def get_name():
    return '🏆 ranker'


def paint():
    st.session_state['ranker_relatedness'] = st.slider('relatedness', -1., 1., 0.8, 0.01, help='the weight of semantic relatedness to the query')
    st.session_state['ranker_activation'] = st.slider('activation', -1., 1., 0., 0.01, help='the weight of thought activation')
    st.session_state['ranker_noise'] = st.slider('noise', 0., 0.1, 0.01, 0.001, help='the amount of noise added')

    # relatedness = st.slider('relatedness', -1., 1., 0.8, 0.01, help='the weight of semantic relatedness to the query')
    # activation = st.slider('activation', -1., 1., 0., 0.01, help='the weight of thought activation')
    # st.session_state['ranker_noise'] = st.slider('noise', 0., 0.1, 0.01, 0.001, help='the amount of noise added')

    # if st.button('set'):
    #     st.session_state['ranker_relatedness'] = relatedness
    #     st.session_state['ranker_activation'] = activation
    #     st.session_state['ranker_noise'] = noise