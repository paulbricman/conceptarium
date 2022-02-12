import importlib
import streamlit as st
from components import header, viewport
from components import microverses
import json


st.set_page_config(
    page_title='💡 conceptarium',
    layout='wide')

microverses.paint()
header.paint()

layout = st.session_state['layout']

col_count = layout['viewportCols'] + \
    int(len(layout['leftColumn']) > 0) + int(len(layout['rightColumn']) > 0)
cols = st.columns(col_count)

for component in layout['leftColumn']:
    with cols[0]:
        m = importlib.import_module('components.' + component)
        with st.expander(component, True):
            m.paint()

for component in layout['rightColumn']:
    with cols[-1]:
        m = importlib.import_module('components.' + component)
        with st.expander(component, True):
            m.paint()

start_viewport_col = int(len(layout['leftColumn']) > 0)
end_viewport_col = start_viewport_col + layout['viewportCols']
viewport.paint(cols[start_viewport_col:end_viewport_col])
