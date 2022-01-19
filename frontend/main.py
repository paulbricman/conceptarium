import streamlit as st
from components import header, inspector, navigator, viewport, ranker
from components import microverses


st.set_page_config(
    page_title='💡 conceptarium',
    layout='wide')


microverses.paint()
header.paint()

cols = st.columns(5)

for component in [navigator, ranker]:
    with cols[0]:
        with st.expander(component.get_name(), True):
            component.paint()

for component in [inspector]:
    with cols[-1]:
        with st.expander(component.get_name(), True):
            component.paint()

viewport.paint(cols[1:-1])
