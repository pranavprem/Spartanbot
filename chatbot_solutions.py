"""Small-talk replies trained as one conversation chain.

ChatterBot 0.6 (the 2017 dependency) does not run on Python 3.12. ListTrainer
stored each line as the reply to the previous line, and LowConfidenceAdapter
returned an empty string below 0.65 similarity so the greensheet path could
take over. This module keeps that chain and that threshold, using
``difflib.SequenceMatcher`` instead of the abandoned library.
"""

import difflib

CONVERSATION = [
    "How are you?",
    "I am good.Thankyou.",
    "That is good to hear.",
    "Thank you",
    "You are welcome.",
    "Whats your name?",
    "I have no name.",
    "Where are you?",
    "I am in California.",
    "Hi",
    "Hello",
    "Hello",
]

THRESHOLD = 0.65


def training_pairs():
    return list(zip(CONVERSATION, CONVERSATION[1:]))


class chatbot_solutions(object):
    def __init__(self):
        self.pairs = training_pairs()

    def chatbot_response(self, sentence):
        if not sentence:
            return ""
        query = sentence.strip().lower()
        best_score = 0.0
        best_response = ""
        for prompt, response in self.pairs:
            score = difflib.SequenceMatcher(None, query, prompt.lower()).ratio()
            if score > best_score:
                best_score = score
                best_response = response
        if best_score >= THRESHOLD:
            return best_response
        return ""
