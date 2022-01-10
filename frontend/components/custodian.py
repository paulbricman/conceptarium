import streamlit as st
import streamlit_authenticator as stauth
import os
import json


def paint():
    with st.sidebar:
        st.markdown('#### 📜 custodian')

        if not os.path.exists('records/custodian.json'):
            st.warning(
                'This appears to be a fresh conceptarium instance. Please create a custodian account.')

            username = st.text_input('Username')
            password = st.text_input('Password', type='password')

            if st.button('create account'):
                password = stauth.hasher([password]).generate()[0]
                token = stauth.hasher([password + 'token']).generate()[0]
                json.dump({
                    'username': username,
                    'password': password,
                    'token': token
                }, open('records/custodian.json', 'w'))
                st.balloons()
        else:
            st.warning(
                'If you\'re the custodian of this conceptarium, please log into your account to access your stored thoughts.')
            custodian = json.load(open('records/custodian.json'))
            authenticator = stauth.authenticate([custodian['username']], [custodian['username']], [custodian['password']],
                                                'custodian_cookie', 'conceptarium', cookie_expiry_days=30)
            name, authentication_status = authenticator.login(
                'login', 'sidebar')

            if st.session_state['authentication_status']:
                st.markdown('')
                st.markdown('##### token')
                st.code(custodian['token'], language='text')
            elif st.session_state['authentication_status'] == False:
                st.error('Username/password is incorrect')
            elif st.session_state['authentication_status'] == None:
                st.warning('Please enter your username and password')
