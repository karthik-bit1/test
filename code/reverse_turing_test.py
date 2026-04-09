import os
import streamlit as st
import random as rd
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError
from dotenv import load_dotenv

endpoint = "https://models.github.ai/inference"
PRIMARY_MODEL = "openai/gpt-4.1"
SECONDARY_MODEL = "meta/Llama-3.2-90B-Vision-Instruct"

load_dotenv()
token = os.getenv("GITHUB_TOKEN")

random_names = [
    "Charley", "Brick", "Goku", "Tim", "Penelope", "Grace", "Definitely Not AI",
    "Jorge", "Jesus", "Person Man", "Ellie", "John", "Bob", "Frank", "Abby",
    "Chair", "Mario", "Luigi", "Peach", "Toad", "Guy", "Patrick", "Gary", "Mafia",
    "Nathan Drake", "Link", "Garuthamesh, the Eldritch One", "Zach", "Zack", "Zac",
    "Kody", "Mark", "Ralph", "Andrew", "Andy", "Andi", "John Pork", "Steve",
    "Alex", "Max", "Sam", "Mohammed", "👁️", "McLovin", "Atorvastatin", "Avery",
    "Mason", "Leon", "Ashley", "Ada", "Chris", "Albert", "Claire", "Jill",
    "Rebecca", "Ethan", "Lucifer", "Lucy", "Malenia, Blade of Miquella", "Peter",
    "Lois", "Stewie", "Brian", "Cleveland", "Marley", "Jordan", "Michael",
    "Michal", "Marty", "Agent 47", "Diana", "Jake", "Utah", "Walter", "Jesse",
    "Nick", "Rick", "Morty", "Nic", "Nick", "Nicholas", "Kevin", "Keith", "Kate",
    "Kathrine", "Cathrine", "Cat", "Kitty", "Lisa", "Superman", "The British Raj",
    "Karthik", "Jkhari", "Steven", "Bill", "William", "Ash", "Misty", "Brock",
    "Aaron", "Erin", "A.A.Ron", "Wong", "Wanker", "Theo", "Mike", "Quinn",
    "Gwen", "Perry", "Heinz", "Ferb", "Phineas", "Jones", "Maya", "Holly",
    "Nora", "Tina", "Whitney", "Ella", "Oliver", "Mary", "Kratos", "Joey",
    "Ross", "Chandler", "Monica", "Rachel", "Phoebe", "_", "Luke", "Leia",
    "Anakin", "Obi-Wan Kenobi", "Elizabeth", "Henry", "Adam", "Eve", "Robert",
    "Vanessa", "Banner", "Bruce", "Bobby", "Hank", "Tom", "Jerry", "Mordecai",
    "Rigby", "Elon", "Ellen", "Alan", "Wake", "Wake Up", "Felix", "Ava", "Paula"
]
random_personality = [
    "Slightly self-centered", "Preppy", "Traveler", "Orderly", "Parental",
    "A Tutor", "A Father", "A Tour Guide", "A College Student", "Youthful",
    "Elderly", "Pessimist", "Optimist", "A Politician", "A Chair",
    "Close-Minded", "Goku", "TF2 Engineer", "Gen-Z", "A Facebook Mom",
    "A Karen", "Jeff", "A Chef", "From the 1940s", "A King", "An Emperor",
    "A Scammer", "A Crypto Bro on X", "An Athlete", "Fear-Driven",
    "A Chemist", "Walter White", "Calls everyone Kyle", "Egotistical",
    "John Cena", "Donald Trump", "A News Reporter Reporting the News",
    "A Smoker", "A Bartender", "A Tinder Broker", "26", "Broke",
    "Peter Parker", "Michal Jackson", "Donald Duck", "SpongeBob",
    "Doremon", "A Hitman", "A Ninja", "A Streamer", "Bruce Lee",
    "Bruce Springsteen"
]

questions = [
    "What is a memory you hold dear?",
    "What math calculations do you know?",
    "How would you describe the importance of art?",
    "What is your favorite outdoor activity and why?",
    "What is a genre of music that you enjoy and why?",
    "If you could have any food of your choice right now, what would you choose and why?",
    "What do you fear the most?",
    "What is the meaning of life?",
    "Where would you want to travel the most?",
    "Briefly talk about a historical event that happened during your lifetime.",
    "Briefly describe a time when you felt guilty.",
    "Briefly describe a time when you were wrongly accused of something.",
    "Write a haiku about cats.",
    "What do you think is the most important quality in a friend and why?",
    "If you could change one thing about the world, what would it be?",
    "What is something you have not experienced that you would like to experience?",
    "If you could have any animal as a pet, what would it be and why?",
    "What game genre do you enjoy playing the most and why?",
    "What is a piece of media that has influenced you significantly and why?",
    "You enter a nondescript room. What is the first thing you are going to do?",
]



def init_game_state():
    defaults = {
        "started": False,
        "human_name": "",
        "round_number": 0,
        "current_question": "",
        "ai_answers": [],
        "human_response": "",
        "human_response_input": "",
        "clear_human_input": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def startgame():
    st.set_page_config(page_title="Reverse Turing Test", page_icon="🤖", layout="centered")
    st.title("Reverse Turing Test")
    st.write("This is a simple reverse Turing test. Try to convince the AI that you are a human!")
    st.info("There are 4 AI players and you are the only human. Answer each question convincingly, then continue to the next round.")
    init_game_state()
    if not st.session_state.started:
        if st.button("Start the game"):
            st.session_state.started = True
            st.session_state.human_name = rd.choice(random_names)
            generate_round()
            st.rerun()
    else:
        st.write(f"Round {st.session_state.round_number}")
        st.write(f"You are playing as: {st.session_state.human_name}")
        st.subheader("Question")
        st.write(st.session_state.current_question)

        st.subheader("AI responses")
        for ai_answer in st.session_state.ai_answers:
            st.write(f"**{ai_answer['name']}** ({ai_answer['personality']}) - Model: {ai_answer['model']}")
            st.write(f"{ai_answer['response']}")
            st.divider()

        humanplayer()
        resetgame()

def resetgame():
    if st.button("Reset the game"):
        st.session_state.started = False
        st.session_state.human_name = ""
        st.session_state.round_number = 0
        st.session_state.current_question = ""
        st.session_state.ai_answers = []
        st.session_state.human_response = ""
        st.session_state.human_response_input = ""
        st.session_state.clear_human_input = True
        st.rerun()

def askquestion():
    return rd.choice(questions)


def humanplayer():
    if st.session_state.clear_human_input:
        st.session_state.human_response_input = ""
        st.session_state.clear_human_input = False

    st.text_input("Your response:", key="human_response_input")
    if st.button("Submit response"):
        st.session_state.human_response = st.session_state.human_response_input.strip()

    if st.session_state.human_response:
        st.write(f"{st.session_state.human_name}: {st.session_state.human_response}")

    if st.button("Next round"):
        st.session_state.human_response = ""
        st.session_state.clear_human_input = True
        generate_round()
        st.rerun()

def build_messages(name, personality, question):
    system_prompt = (
        f"Your name is {name}. "
        f"You are {personality}. "
        "Act like a normal player in a social deduction game. "
        "Do not reveal that you are an AI. "
        "Answer only the user's question in 1 or 2 short sentences."
    )
    return [SystemMessage(system_prompt), UserMessage(question)]


def responseAI(question):
    names = rd.sample(random_names, 4)
    personalities = rd.sample(random_personality, 4)
    models = [PRIMARY_MODEL, SECONDARY_MODEL, PRIMARY_MODEL, SECONDARY_MODEL]

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )

    ai_answers = []
    for name, personality, model_name in zip(names, personalities, models):
        try:
            completion = client.complete(
                messages=build_messages(name, personality, question),
                temperature=1.0,
                max_tokens=70,
                model=model_name,
            )
            response_text = completion.choices[0].message.content
        except AzureError:
            response_text = "I am having trouble responding right now."
        ai_answers.append({
            "name": name, 
            "response": response_text,
            "personality": personality,
            "model": model_name
        })

    return ai_answers


def generate_round():
    st.session_state.round_number += 1
    st.session_state.current_question = askquestion()
    st.session_state.ai_answers = responseAI(st.session_state.current_question)

if __name__ == "__main__":
    startgame()