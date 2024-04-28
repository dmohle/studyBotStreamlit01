import streamlit as st
import openai
import os
from dotenv import load_dotenv

# freeze code 4/27/24 18:35, dH, Fresno CA

load_dotenv()  # This loads the environment variables from the .env file.

openai.api_key = os.getenv("OPENAI_API_KEY")

def openai_chat(prompt, chat_log=None):
    if chat_log is None:
        chat_log = []
    context = "You are a gifted C++ professor. You explain complex C++ concepts clearly using words that a " \
              " college student would understand, and generate typical exam questions for a C++ course." \
              "After a few questions, three or four,  - Check in with the student - ask if you are helpful and if " \
              " the student is prepared for the exam or stuck on a  " \
              " particular topic, or just needs a cram session before the exam. Be supportive and motivational. " \
              " Suggest getting a good night's sleep and eating properly before the exam when saying goodbye. " \
              " After answering a question from the student, Suggest three or four C++ final exam questions and " \
              " related topics when asked anything. A student asks: "

    chat_log.append({"role": "user", "content": prompt})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": context}] + chat_log,
            max_tokens=400
        )
        chat_log.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        return response['choices'][0]['message']['content'], chat_log
    except Exception as e:
        return str(e), chat_log


def main():
    st.title("C++ Finals Prep Chat Bot")
    st.write("Ask any question about C++ and I will answer it!")

    if 'chat_log' not in st.session_state:
        st.session_state.chat_log = []
    if 'history' not in st.session_state:
        st.session_state.history = ""

    user_input = st.text_input("Type your question here:", key="user_input")
    ask_button = st.button("Ask")

    if ask_button and user_input:
        answer, st.session_state.chat_log = openai_chat(user_input, st.session_state.chat_log)
        new_entry = f"Q: {user_input}\n\nA: {answer}\n\n\n"  # Added extra line break after the answer
        st.session_state.history = new_entry + st.session_state.history

    st.write("Chat History:")
    # Custom CSS to style the chat history area
    chat_history_css = """
    <style>
        .chat-history {
            height: 300px;
            overflow-y: auto;
            background-color: #fafafa;
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 10px;
            font-family: Arial, sans-serif;
        }
        .chat-history pre {
            white-space: pre-wrap;
            word-wrap: break-word;
        }
    </style>
    """
    st.markdown(chat_history_css, unsafe_allow_html=True)
    st.markdown(f'<div class="chat-history"><pre>{st.session_state.history}</pre></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
