import streamlit as st
from components import custodian, header, inspector, navigator, viewport, ranker
import uvicorn


st.set_page_config(
    page_title='💡 conceptarium',
    layout='wide',
    menu_items={
        'About': 'hello world'
    })


# if not hasattr(st, 'already_started_server'):
#     # Hack the fact that Python modules (like st) only load once to
#     # keep track of whether this file already ran.
#     st.already_started_server = True

#     st.write('''
#         The first time this script executes it will run forever because it's
#         running a Flask server.

#         Just close this browser tab and open a new one to see your Streamlit
#         app.
#     ''')

#     from flask import Flask

#     app = Flask(__name__)

#     @app.route('/foo')
#     def serve_foo():
#         return 'This page is served via Flask!' + str(st.session_state['authentication_status'])

#     app.run(port=8888)

#     # from fastapi import FastAPI

#     # app = FastAPI()

#     # @app.get("/")
#     # async def root():
#     #     return {"message": "Hello World"}

#     # print('running next')
#     # uvicorn.run(app, port=8888)
#     # print('ran')


custodian.paint()
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
