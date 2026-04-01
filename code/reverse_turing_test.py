import os
import streamlit as st
def main():
    st.set_page_config(page_title="Reverse Turing Test", page_icon="🤖", layout="centered")
    st.title("Reverse Turing Test")
    st.write("This is a simple reverse Turing test. Try to convince the AI that you are a human!")
    st.info("There are 4 AI's, you are the ONLY human. You will be asked  a series of questions and you must convince the AI's that you are one of them. Your goal is to vote all AI out of the game. Good Luck!")
    if 'started' not in st.session_state:
        st.session_state.started = False

    if not st.session_state.started:
        if st.button("Start the game"):
            st.session_state.started = True
            st.rerun()
    else:
        name = st.text_input("What is your name?")
        if name:
            st.write(f"Welcome, {name}. The AIs are watching...")

if __name__ == "__main__":
    main()
