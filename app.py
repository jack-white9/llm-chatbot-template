import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import os


def setup():
    st.title("LLM Chatbot")
    load_dotenv()


def initialize_session_state():
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
    if "messages" not in st.session_state:
        st.session_state.messages = []


def display_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def get_user_input():
    prompt = st.chat_input("Type message...")
    return prompt


def interact_with_openai(prompt):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})


def main():
    setup()
    initialize_session_state()
    display_messages()
    prompt = get_user_input()
    if prompt:
        interact_with_openai(prompt)


if __name__ == "__main__":
    main()
