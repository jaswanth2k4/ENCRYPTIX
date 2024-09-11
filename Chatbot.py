import streamlit as st
import json
import random


def json_dataset(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def txt_dataset(filename):
    dataset = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue  
            parts = line.split('\t')
            if len(parts) != 2:
                print(f"Skipping malformed line: {line}")
                continue 
            
            tag, responses = parts
            dataset[tag] = {
                "patterns": [],  
                "responses": responses.split('\t')  
            }
    return dataset


def combine_datasets(json_data, txt_data):
    combined_data = {}

    for intent in json_data["intents"]:
        tag = intent["tag"]
        combined_data[tag] = {
            "patterns": intent["patterns"],
            "responses": intent["responses"]
        }

    for tag, intent in txt_data.items():
        if tag in combined_data:
            combined_data[tag]["responses"].extend(intent["responses"])
        else:
            combined_data[tag] = intent

    return combined_data

def get_response(user_input, dataset):
    user_input = user_input.lower()
    print(f"User input: {user_input}")  # Debugging line
    
    for tag, intent in dataset.items():
        print(f"Checking tag: {tag}")  # Debugging line
        for pattern in intent["patterns"]:
            print(f"Checking pattern: {pattern}")  # Debugging line
            if pattern.lower() in user_input:
                print(f"Pattern matched: {pattern}")  # Debugging line
                return random.choice(intent["responses"])
    
    return None

json_data = json_dataset('dataset.json')  
txt_data = txt_dataset('dataset.txt')      


dataset = combine_datasets(json_data, txt_data)


st.title("Simple Rule-Based Chatbot")

user_input = st.text_input("You: ", placeholder="Type your message here...")

if user_input:
    response = get_response(user_input, dataset)
    if response:
        st.text_area("Chatbot:", value=response, height=100, max_chars=None, key=None)
    else:
        st.text_area("Chatbot:", value="Sorry, I didn't understand that. Can you please ask something else?", height=100, max_chars=None, key=None)
