import streamlit as st
from components import core, inspector, navigator, viewport
import streamlit.components.v1 as components

st.set_page_config(
    page_title='💡 conceptarium',
    layout='wide')

top = st.empty()

core.header_section()
core.footer_section()

cols = st.columns([1, 1, 1, 1])
layout = [[navigator], [viewport], [], [inspector]]

for col_idx, col in enumerate(layout):
    for component in col:   
        with cols[col_idx]:
            with st.expander(component.get_name(), True):
                component.paint()