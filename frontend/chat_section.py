import streamlit as st
import time

class Chat_with_AI:

    def start_chatting(self):
        if "messages" not in st.session_state:
            st.session_state.messages = [] 

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


        if prompt := st.chat_input("Upload your Resume and start getting tested"):
            st.session_state.messages.append({"role":"user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                assistance_response = f"You said : '{prompt}'. Here we will get the response from AI "

                for chunk in assistance_response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    message_placeholder.markdown(full_response+"▌")

                message_placeholder.markdown(full_response)

            st.session_state.messages.append({"role": "Assistant", "content": full_response})

chat_bro = Chat_with_AI()