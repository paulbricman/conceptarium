import streamlit as st
import pickle


def load():
    if st.session_state['authentication_status']:
        thoughts = pickle.load(open('conceptarium/metadata.pickle', 'rb'))
        return thoughts
    else:
        return []
