import streamlit as st
from components import core, inspector, navigator, viewport
import streamlit.components.v1 as components

st.set_page_config(
    page_title='💡 conceptarium',
    layout='wide')

top = st.empty()

core.header_section()
core.footer_section()

cols = st.columns([1, 1, 1, 1, 1])
left_section = [navigator]
right_section = [inspector]

viewport.paint(cols[1:-1])

for component in left_section:   
    with cols[0]:
        with st.expander(component.get_name(), True):
            component.paint()

for component in right_section:   
    with cols[-1]:
        with st.expander(component.get_name(), True):
            component.paint()