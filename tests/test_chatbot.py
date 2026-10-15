from chatbot_solutions import chatbot_solutions


def test_conversation_chain_and_empty_fallback():
    bot = chatbot_solutions()
    assert bot.chatbot_response("How are you?") == "I am good.Thankyou."
    assert bot.chatbot_response("thank you") == "You are welcome."
    assert bot.chatbot_response("hi") == "Hello"
    assert bot.chatbot_response("zzzz-not-a-trained-line") == ""
