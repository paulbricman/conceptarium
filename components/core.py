import streamlit as st


def header_section():
    st.markdown('### 💡 conceptarium')
    
    
def footer_section():
    hide_streamlit_style = '''
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                '''
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)