import streamlit as st
import json
import requests
from chat_section import chat_bro

def registration():import streamlit as st
import json
import requests
from chat_section import chat_bro

def registration():
    # Initialize session state if not exists
    if 'show_form' not in st.session_state:
        st.session_state.show_form = False

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Register"):
            st.session_state.show_form = True
    with col2:
        if st.button("Try it"):
            chat_bro.start_chatting()

    # Show form only if Register was clicked
    if st.session_state.show_form:
        with st.form("Signup"):
            username: str = st.text_input("Give your self Username")
            email: str = st.text_input("Your email")
            password: str = st.text_input("Password make sure u remember this", type="password")
            if submitted := st.form_submit_button("Submit"):
                sending = {
                    'UserName': username,
                    'Email': email,
                    'Password': password
                }
                
                try:
                    res = requests.post("http://localhost:5000/api/reg", 
                                      json=sending,
                                      headers={"Content-Type": "application/json"})

                    try:
                        response_data = res.json()
                        if res.status_code == 201:
                            st.success("Registration successful! 🎉")
                            st.session_state.show_form = False  # Hide the form
                            st.rerun() 
                        else:
                            st.error(f"Registration failed: {response_data.get('detail', 'Unknown error')}")
                    except json.JSONDecodeError:
                        st.error(f"Invalid response from server: {res.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Request Failed: {str(e)}")