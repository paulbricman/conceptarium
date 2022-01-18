import streamlit as st


def paint():
    with st.sidebar:
        st.markdown('## 🌐 microverses')

        microverses = st.session_state.get('microverses', [])

        if len(microverses) > 0:
            st.markdown('---')
            st.markdown('### current microverses')

            for e_idx, e in enumerate(microverses):
                st.code(e[0])
                if st.button('remove', key=(e, e_idx)):
                    st.session_state['microverses'] = st.session_state.get(
                        'microverses', [])
                    st.session_state['microverses'].remove(e)
                    st.experimental_rerun()

        st.markdown('---')
        st.markdown('### add new microverse')

        url = st.text_input('conceptarium url')
        token = st.text_input('microverse token')

        if st.button('add'):
            st.session_state['microverses'] = st.session_state.get(
                'microverses', []) + [(url, token)]
            st.experimental_rerun()
