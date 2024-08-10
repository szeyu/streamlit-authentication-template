import streamlit as st

def init_session():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'
    if 'guest_mode' not in st.session_state:
        st.session_state['guest_mode'] = False
    if 'verifying' not in st.session_state:
        st.session_state['verifying'] = False
    if 'otp' not in st.session_state:
        st.session_state['otp'] = ""
    if 'email' not in st.session_state:
        st.session_state['email'] = ""
    if 'password' not in st.session_state:
        st.session_state['password'] = ""
    if 'extra_input_params' not in st.session_state:
        st.session_state['extra_input_params'] = {}
        
    

def reset_session():
    st.session_state['authenticated'] = False
    st.session_state['page'] = 'login'
    st.session_state['guest_mode'] = False
    st.session_state['verifying'] = False
    st.session_state['otp'] = ""
    st.session_state['email'] = ""
    st.session_state['password'] = ""
    
    for input_param in st.session_state['extra_input_params'].keys():
        if input_param not in st.session_state:
            st.session_state[input_param] = None
