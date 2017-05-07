"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function

import random, re

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "NewGame":
        return start_new_game(intent, session)
    elif intent_name == "RepeatCategory":
        return repeat_category(intent, session)
    elif intent_name == "GuessLetter":
        return intent_guess_letter(intent, session)
    elif intent_name == "GuessWord":
        return intent_guess_word(intent, session)
    elif intent_name == "EndGame":
        return intent_end_game(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Skills Kit sample. " \
                    "Please tell me your favorite color by saying, " \
                    "my favorite color is red"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me your favorite color by saying, " \
                    "my favorite color is red."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))



words = [
    ("Animal", "cat"),
    ("Animal", "dog"),
    ("Animal", "snake"),
    ("Animal", "elephant"),
    ("Animal", "swan"),
    ("Animal", "seagull"),
    ("Animal", "worm"),
    ("Animal", "medusa"),
    ("Animal", "hamster"),
    ("Animal", "rabbit"),
    ("Food", "cake"),
    ("Food", "pizza"),
    ("Food", "spaghetti"),
    ("Food", "sandwich"),
    ("Food", "youghurt"),
    ("Food", "chocolate"),
    ("Food", "crisps"),
    ("Food", "chips"),
    ("Food", "burger"),
    ("Sport", "football"),
    ("Sport", "surfing"),
    ("Sport", "rugby"),
    ("Sport", "basketball"),
    ("Sport", "baseball"),
    ("Sport", "cricket"),
    ("Sport", "cycling"),
    ("Sport", "sailing"),
    ("Transportation", "car"),
    ("Transportation", "plane"),
    ("Transportation", "boat"),
    ("Transportation", "bus"),
    ("Transportation", "underground"),
    ("Transportation", "tram"),
    ("Transportation", "bicycle"),
    ("Transportation", "rocket"),
    ("Colors", "red"),
    ("Colors", "green"),
    ("Colors", "blue")
    ("Colors", "black")
    ("Colors", "white")
    ("Colors", "pink")
    ("Colors", "violet")
    ("Colors", "orange")
    ("Colors", "grey")
]

def get_tries(session):
    tries = session.get('attributes', { "tries": 0 })["tries"]
    if tries == 0:
        return " You have no tries. "
    elif tries == 1:
        return random.choice([
            " Beware, this is your last try. ",
            "This is your last try.",
            "One more fail and you lose."
        ])
    else:
        return " You have " + str(tries) + " tries. "

def intent_guess_word(intent, session):
    session_attributes = session.get('attributes', {})
    reprompt_text = get_repromt(intent, session)
    should_end_session = False
    
    if session.get('attributes', {}) and "category" in session.get('attributes', {}):
        word_guessed = intent["slots"]["Word"]["value"]
        
        guessed_word = session.get("attributes", { })["guessed_word"]
        word = session.get("attributes", { })["word"]
        if len(word) != len(word_guessed):
            speech_output = "Your word has " + str(len(word_guessed)) + " letters and mine has " + str(len(word)) + ". Wrong word"
        elif len(word) == len(word_guessed) and re.match(guessed_word, word_guessed):
            if word == word_guessed:
                speech_output = random.choice([
                    "Congratulations! This is it!",
                    "Good job! You got it!",
                    "Damn you are good. You guessed!",
                    "Wow you got it. Much respect!",
                    "Cool, you got it!"
                    ])
                should_end_session = True
            else:
                session_attributes["tries"] -= 1
                speech_fragment = random.choice([
                    "Nope, this is wrong.",
                    "Not this time, wrong answer.",
                    "That's not what I meant",
                    "Sorry, wrong word."
                    ])
                speech_output = speech_fragment + get_tries(session)
        else:
            speech_output = "I didn't understand your word. I understood " + word_guessed + ". Please try again." + get_tries(session)
    else:
        speech_output = "The game is not started yet. Tell me to start a new game."
    word = session.get("attributes", { })["word"]
    if session_attributes["tries"] <= 0 :
        speech_output = "I am sorry but you lost, you looser. The word I meant was " + word + " . Yes, it was that simple."
        should_end_session = True
    
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
    
def intent_guess_letter(intent, session):
    session_attributes = session.get('attributes', {})
    reprompt_text = get_repromt(intent, session)
    should_end_session = False
    
    if session.get('attributes', {}) and "category" in session.get('attributes', {}):
        l = intent["slots"]["Letter"]["value"]
        letter = ""
        for x in l:
            if x.isalpha():
                letter = x.lower()
                break
        if letter.isalpha() and len(letter) == 1:
            guessed_word = session.get("attributes", { })["guessed_word"]
            word = session.get("attributes", { })["word"]
            new_guessed_word = ""
            found_letter = False
            penalty = True
            for i in range(len(word)):
                if word[i] == letter:
                    penalty = False
                    new_guessed_word += word[i]
                    if guessed_word[i] == '.':
                        found_letter = True
                else:
                    new_guessed_word += guessed_word[i]
            session_attributes["guessed_word"] = new_guessed_word
            if word == new_guessed_word :
                speech_output = " Congratulations! You guessed the word: " + word
                should_end_session = True
            else:
                if found_letter:
                    speech_output = "Great, your word is <say-as interpret-as='spell-out'>" + new_guessed_word + "</say-as>" + get_tries(session)
                else:
                    if penalty:
                        session_attributes["tries"] -= 1
                        speech_output = "Sorry, there is no " + letter + " in my word. Again the word is <say-as interpret-as='spell-out'>" + new_guessed_word + "</say-as>" + get_tries(session)
                    else:    
                        speech_output = "Well there is no more " + letter + " in my word. Again the word is <say-as interpret-as='spell-out'>" + new_guessed_word + "</say-as>" + get_tries(session)
        else:
            speech_output = "I didn't understood your letter. I understood <say-as interpret-as='spell-out'>" + l + "</say-as>. Please try again." + get_tries(session)
    else:
        speech_output = "The game is not started yet. Tell me to start a new game."
    word = session.get("attributes", { })["word"]
    if session_attributes["tries"] <= 0 :
        speech_output = "I am sorry but you lost, you looser. The word I meant was " + word + " . Yes, it was that simple."
        should_end_session = True
    
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
    
def intent_end_game(intent, session):
    speech_output = "The game has ended"
    reprompt_text = get_repromt(intent, session)
    should_end_session = True
    return build_response({}, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))    

def get_repromt(intent, session):
    return "Tell me a letter"
    
def repeat_category(intent, session):
    session_attributes = session.get('attributes', {})
    reprompt_text = get_repromt(intent, session)

    if session.get('attributes', {}) and "category" in session.get('attributes', {}):
        speech_output = "Your category is " + session['attributes']['category']
    else:
        speech_output = "The game is not started yet. Tell me to start a new game."
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
def start_new_game(intent, session):
    session_attributes = session.get('attributes', {})
    reprompt_text = get_repromt(intent, session)
    
    if session.get('attributes', {}) and "category" in session.get('attributes', {}):
        speech_output = "Game is already started. If you want to start a new game, firstly end this game"
    else:
        game = random.choice(words)
        session_attributes = {
            "category": game[0],
            "word": game[1],
            "guessed_word": "." * len(game[1]),
            "tries": 10
        }
        speech_output = "I guessed a word from category " + game[0] + " that has " + str(len(game[1])) + " letters."
    
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': '<speak>' + output + '</speak>'
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }



def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }