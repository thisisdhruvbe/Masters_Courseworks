import numpy as np
from keras.models import load_model
import json
import pickle
import nltk
from nltk.stem import WordNetLemmatizer

# Load the trained model, words, and classes
model = load_model('chatbot_model.h5')
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

# Load the intents file
intents = json.loads(open('intents.json').read())

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Function to preprocess the user input
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# Function to convert input to bag of words
def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

# Function to predict the intent of the user input
def predict_class(sentence, model):
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

# Function to get a response based on the predicted intent
def get_response(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    
    result = "Sorry, I don't have a response for that."  # Default value
    
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    
    return result

#Function to manage Deletion of the contact
def manage_contact_deletion():
    print("Bot: Tell me the name of the contact you want to delete ")
    contact_to_delete = input("You: ")

    if contact_to_delete in contacts:
        del contacts[contact_to_delete]
        print(f"Bot: Contact '{contact_to_delete}' deleted successfully.")
    else:
        print(f"Bot: Contact '{contact_to_delete}' not found. Please check the name.")

# Function to handle discoverability questions
def handle_discoverability_question():
    print("Bot: I am a chatbot designed to assist you. How may I help you today?")

# Function to do identity management
def manage_user_name(message):
    global user_name
    if user_name:
        user_name = message
        print(f"hi {user_name}")
    else:
        new_name = input("can you repeat your name")
        user_name = new_name
        print(f"Bot: hi {new_name}")

import random

# Dictionary to store user-entered contacts
contacts = {}


user_name = None

while True:
    message = input("You: ")
    if message.lower() == 'quit':
        break

    ints = predict_class(message, model)

    if user_name is None:
        # If the user's name is not set, assume the first input is their name
        user_name = message
        print(f"Bot: Hello, {user_name}! How can I assist you today?")
        continue

    if ints[0]['intent'] == 'contact':
        # If the intent is to save a contact, ask for both name and number
        print("Bot: " + get_response(ints, intents))
        name = input("You: ")

        # Wait for user input for the number
        if name:
            number = input("Bot: Please provide the contact number.\nYou: ")
            if number.isdigit():
                contacts[name] = number
                print(f"Bot: Contact '{name}' with number '{number}' saved successfully!")
            else:
                print("Bot: Please enter a valid numerical value for the contact number.")

        # Process the name and number or perform any other relevant action
        
    elif ints[0]['intent'] == 'show_contact':
        # If the intent is to show contacts, retrieve and print them
        if contacts:
            contacts_list = [f"{name}: {number}" for name, number in contacts.items()]
            print("Bot:", get_response(ints, intents).format(contacts=", ".join(contacts_list)))
        else:
            print("Bot: You don't have any contacts yet.")

    elif ints[0]['intent'] == 'modify_contact':
        # If the intent is to modify a contact, ask for the contact name to modify
        print("Bot: " + get_response(ints, intents))
        contact_to_modify = input("You: ")

        if contact_to_modify in contacts:
            # If the contact exists, ask for new details
            print(f"Bot: What do you want to modify for '{contact_to_modify}'?")
            modification_choice = input("You: ")

            if modification_choice.lower() == 'name':
                # Modify the name
                new_name = input("Bot: Please provide the new name.\nYou: ")
                contacts[new_name] = contacts.pop(contact_to_modify)
                print(f"Bot: Contact '{contact_to_modify}' modified to '{new_name}'.")
            elif modification_choice.lower() == 'number':
                # Modify the number
                while True:
                    new_number = input("Bot: Please provide the new number.\nYou: ")
                    if new_number.isdigit():
                        break
                    else:
                        print("Bot: Please enter a valid numerical value for the new number.")
                contacts[contact_to_modify] = new_number
                print(f"Bot: Number for contact '{contact_to_modify}' modified to '{new_number}'.")
            else:
                print("Bot: Sorry, I couldn't understand that. Let's start over.")
        else:
            print(f"Bot: Contact '{contact_to_modify}' not found. Please check the name.")

    elif ints[0]['intent'] == 'discoverability':
        handle_discoverability_question()
    
    elif ints[0]['intent'] == 'manageusername':
        manage_user_name(user_name)

    elif ints[0]['intent'] == 'delete_contact':
        manage_contact_deletion()

    else:
        res = get_response(ints, intents)
        print("Bot:", res)
    
