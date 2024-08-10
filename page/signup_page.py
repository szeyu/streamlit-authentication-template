import streamlit as st
import re
from utils.otp_handler import generate_otp, send_email
from utils.db_handler import save_user, verify_duplicate_user
import time

def is_valid_email(email):
    """Check if the provided email is valid using regex."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def input_field(input_param, type):
    """Render an input field based on the type and store the value in session state."""
    if type == 'text':
        st.session_state[input_param] = st.text_input(input_param)
    elif type == 'number':
        st.session_state[input_param] = st.number_input(input_param, step=1)

def verifyOTP(otp_input):
    """Verify the OTP input by the user."""
    if otp_input == st.session_state['otp']:
        st.success("OTP verified successfully")
        time.sleep(1)
        st.session_state['verifying'] = False
        st.session_state['otp'] = ""
        save_user(st.session_state['email'], st.session_state['password'], st.session_state['extra_input_params'])
        st.session_state['page'] = 'login'
        st.rerun()
    else:
        st.error("Invalid OTP")

def signup_page(extra_input_params=False, confirmPass=False):
    """Render the signup page with optional extra input parameters and password confirmation."""
    if st.session_state['verifying']:
        # Check if the user already exists
        if verify_duplicate_user(st.session_state['email']):
            st.error("User already exists")
            time.sleep(1)
            st.session_state['verifying'] = False
            st.rerun()
        
        st.write("Verifying OTP...")
        st.info(f"OTP has been sent to {st.session_state['email']}")
        print(st.session_state['otp'])
        if st.session_state['otp'] == "":
            st.session_state['otp'] = generate_otp()
            print(st.session_state['otp'])
            send_email(st.session_state['email'], st.session_state['otp'])
                
        with st.empty().container():
            otp_input = st.text_input(label="Enter OTP", placeholder="Enter OTP")
            if st.button("Verify OTP"):
                verifyOTP(otp_input)
                
            if st.button("Resend OTP"):
                sent = False
                st.session_state['otp'] = generate_otp()
                send_email(st.session_state['email'], st.session_state['otp'])
        
    else:
        if st.button("Back to Login"):
            st.session_state['page'] = 'login'
            st.rerun()
        
        with st.empty().container(border=True):
            st.title("Sign Up Page")
            
            # Email input with validation
            st.session_state['email'] = st.text_input("Email")
            if st.session_state['email'] and not is_valid_email(st.session_state['email']):
                st.error("Please enter a valid email address")

            # Password input
            st.session_state['password'] = st.text_input("Password", type='password')
            
            # Confirm password if required
            if confirmPass:
                confirm_password = st.text_input("Confirm Password", type='password')
            
            # Extra input fields if any
            if extra_input_params:
                for input_param, type in st.session_state['extra_input_params'].items():
                    input_field(input_param, type)
            
            # Validate all required fields before proceeding
            if st.session_state['email'] and st.session_state['password'] and \
               (not confirmPass or (confirmPass and st.session_state['password'] == confirm_password)):
                
                if extra_input_params and not all(st.session_state.get(param) for param in st.session_state['extra_input_params']):
                    st.error("Please fill in all required fields")
                else:
                    if st.button("Register"):
                        st.session_state['verifying'] = True
                        st.rerun()
            else:
                if confirmPass and st.session_state['password'] != confirm_password:
                    st.error("Passwords do not match")
                elif st.button("Register"):
                    st.error("Please fill in all required fields")
