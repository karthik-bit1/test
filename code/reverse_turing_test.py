import os
import streamlit as st
import random as rd
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import AssistantMessage, SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError
from dotenv import load_dotenv

endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"
model1 = "meta/Llama-3.2-90B-Vision-Instruct"

load_dotenv()
token = os.getenv("GITHUB_TOKEN")

random_names= ["rubby", "marry", "jim", "maron", "lisa", "lucy", "tom", "jerry", "bob", "alice"]
name1, name2, name3, name4, name5= rd.sample(random_names, 5)


def startgame():
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
        responseAI()
        humanplayer()

def humanplayer():
    response  = st.text_input("your response: ")
    if response:
        st.write(f"{name5}: {response}")

def responseAI():
    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )
    message1 = [
        SystemMessage(f"You name is {name1}. Your thing is to find who the human out of all the players. And you are restricted to say you are an AI. You are only allowed to answer the question and tell nothing else"),
        UserMessage("What is your name?"),
    ]

    message2 = [
        SystemMessage(f"You name is {name2}. Your thing is to find who the human out of all the players. And you are restricted to say you are an AI. You are only allowed to answer the question and tell nothing else"),
        UserMessage("What is your name?"),
    ]

    message3 = [
        SystemMessage(f"You name is {name3}. Your thing is to find who the human out of all the players. And you are restricted to say you are an AI. You are only allowed to answer the question and tell nothing else"),
        UserMessage("What is your name?"),
    ]

    message4 = [
        SystemMessage(f"You name is {name4}. Your thing is to find who the human out of all the players. And you are restricted to say you are an AI. You are only allowed to answer the question and tell nothing else"),
        UserMessage("What is your name?"),
    ]

    response1 = client.complete(
            messages=message1,
            temperature=1.0,
            max_tokens=100,
            model=model,
        )
    
    response2 = client.complete(
            messages=message2,
            temperature=1.0,
            max_tokens=100,
            model=model1,
        )
    
    response3 = client.complete(
            messages=message3,
            temperature=1.0,
            max_tokens=100,
            model=model,
        )
    response4 = client.complete(
            messages=message4,
            temperature=1.0,
            max_tokens=100,
            model=model1,
        )

    response_A1= response1.choices[0].message.content
    response_A2= response2.choices[0].message.content
    response_A3= response3.choices[0].message.content
    response_A4= response4.choices[0].message.content
    st.write("What is your name?")
    st.write(f"{name1}: {response_A1}")
    st.write(f"{name2}: {response_A2}")
    st.write(f"{name3}: {response_A3}")
    st.write(f"{name4}: {response_A4}")
if __name__ == "__main__":
    startgame()

