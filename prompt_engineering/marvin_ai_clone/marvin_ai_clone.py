# See https://github.com/prefecthq/marvin
from openai import OpenAI

from prompts import (
    CLASSIFY_MESSAGES, 
    EXTRACT_MESSAGES,
    GENERATE_MESSAGES, 
    DEFINE_MESSAGES,
    SPELL_CHECK_MESSAGES
)

client = OpenAI()

def fetch_response(messages):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    return completion.choices[0].message.content


def classify(text, labels):
    """
    Classifies given a text and list of labels
    """

    return fetch_response(CLASSIFY_MESSAGES + [{
        "role": "user",
        "content": f"Your text is {text} and your labels are {labels}"
    }])

def extract(text, model):
    """
    Extracts given text and a target pydantic model
    """

    return fetch_response(EXTRACT_MESSAGES + [{
        "role": "user",
        "content": f"Your text is {text} and your model is {model}"
    }])

def generate(n, instruction, model):
    """
    Generates given an instruction, target pydantic model, and number of 
    instances to generate
    """

    return fetch_response(GENERATE_MESSAGES + [{
        "role": "user",
        "content": f"Your instruction is {instruction}, your model is {model}, and n = {n}"
    }])


def define(term):
    """
    Defines a given term, including part of speech
    """

    return fetch_response(DEFINE_MESSAGES + [{
        "role": "user",
        "content": f"Your term is {term}"
    }])

def spellCheck(text):
    """
    Fixes spelling and grammar errors in a text
    """

    return fetch_response(SPELL_CHECK_MESSAGES + [{
        "role": "user",
        "content": f"Your text is {text}"
    }])