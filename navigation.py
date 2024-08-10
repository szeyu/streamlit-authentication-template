import streamlit as st
from page.login_page import login_page
from page.signup_page import signup_page
from page.app import app_page
from utils.init_session import init_session, reset_session

init_session()

st.session_state['extra_input_params'] = {
    'Faculty':'text',
    'Year':'number',
    'Semester':'number',
}
for input_param in st.session_state['extra_input_params'].keys():
    if input_param not in st.session_state:
        st.session_state[input_param] = None


if st.session_state['authenticated']:
    app_page()
else:
    if st.session_state['page'] == 'login':
        reset_session()
        login_page(guest_mode=True)
    elif st.session_state['page'] == 'signup':
        signup_page(
            extra_input_params=True,
            confirmPass = True
        )
