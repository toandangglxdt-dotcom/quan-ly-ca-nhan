import time
import streamlit as st
from google import genai
from google.genai import types

st.title("🤖 Chat bot")

##Gemini
client = genai.Client(api_key = st.secrets["gemini_api_key"])
model = "gemini-3.5-flash"
system = "you'r friendly assistant, answer in vietnamese, breifly and to the point"

def gen_aswer(message):
    history = [
        types.Content(
            role = "user" if mess["role"] == "user" else "model", # GG call AI is "model"
            parts = [types.Part(text = mess["content"])],
        )
        for mess in message
    ]
    stream = client.models.generate_content_stream(
        model = model,
        contents = history,
        config = types.GenerateContentConfig(
            system_instruction = system,
            max_output_tokens = 1000,
        ),
    )
    for piece in stream:
        if piece.text:
            yield piece.text


if "message" not in st.session_state:
    st.session_state.message = []


#Display all chat history
for mess in st.session_state.message:
    with st.chat_message(mess["role"]):
        st.write(mess["content"])


#Input session at end of page
question = st.chat_input("Asking somthing ....")


if question:
    st.session_state.message.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    # AI Simulator
    # def simulator_ai_answer(sentence):
    #     for wor in f"You asked: {sentence}.".split():
    #         yield wor + " "
    #         time.sleep(0.1)

    # with st.chat_message("assistant"):
    #     answer = st.write_stream(simulator_ai_answer(question))

    # AI
    # with st.chat_message("assistant"):
    #     with client.messages.stream(
    #         model = 'claude-sonnet-5-5',
    #         max_tokens = 1000,
    #         system = "you'r friendly assistant, answer in vietnamese, breifly and to the point",
    #         messages = st.session_state.message,
    #     ) as stream:
    #         answer = st.write_stream(stream.text_stream)

    with st.chat_message("assistant"):
        answer = st.write_stream(gen_aswer(st.session_state.message))

    st.session_state.message.append({"role": "assistant", "content": answer})
