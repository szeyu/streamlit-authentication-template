import streamlit as st
from utils.db_handler import get_users
from utils.init_session import reset_session

def app_page():
    with st.sidebar:
        if st.session_state['guest_mode']:
            st.subheader("Guest Mode")
            
            if st.button("Login"):
                reset_session()
                st.rerun()
                
        else:
            if st.button("Logout"):
                reset_session()
                st.rerun()
        
    st.title("App Page")
    st.write("Hello World")
    users = get_users()
    if users:
        st.table(users)
    

