from groq import Groq
import streamlit as st
import json

st.title("ChatBot:speech_balloon:")

st.sidebar.header("ChatBot")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "groq_model" not in st.session_state:
    st.session_state["groq_model"] = "llama3-8b-8192"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I assisst you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        chat_completion = client.chat.completions.create(
            model=st.session_state["groq_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = ""
        
        # Stream the response and display it in real-time
        for mess in chat_completion:
            # Access content directly from the delta object
            content_part = mess.choices[0].delta.content if mess.choices[0].delta.content else ""
            response += content_part  # Accumulate the response content
        st.markdown(response)  # Display the streamed part in real-time

    # Append the assistant's response to the session state
    st.session_state.messages.append({"role": "assistant", "content": response})
