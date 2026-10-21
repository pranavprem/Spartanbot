from controller import controller


def test_smalltalk_returns_before_the_satisfaction_question():
    reply = controller().find_solution("How are you?")
    assert reply == "I am good.Thankyou."


def test_calculator_reply_is_separated_from_the_followup():
    reply = controller().find_solution("do 7 * 6")
    assert reply == "result is 42\nAre you satisfied with that response?"


def test_unknown_question_uses_the_greensheet_template():
    reply = controller().find_solution("zzzz-not-a-trained-line")
    assert reply == (
        "CUSTOM SOLUTION :: \nAdditionally, this might help:\nAre you satisfied with that response?"
    )


def test_no_then_remember_stores_the_sentence(tmp_path):
    bot = controller()
    assert bot.find_solution("no") == "Please enter what you consider a valid response"
    assert bot.find_solution("Office hours are Wednesday") == "I'll remember that"
    from db import spartandb

    sentences = [row["sentence"] for row in spartandb().read()]
    assert "office hours are wednesday" in sentences


def test_google_hits_are_appended_when_the_client_returns_them(monkeypatch):
    bot = controller()

    def fake_search(term, **kwargs):
        assert kwargs["num"] == 1
        return [{"formattedUrl": "https://example.edu/a", "snippet": "A snippet"}]

    monkeypatch.setattr(bot.google_sol, "google_search", fake_search)
    reply = bot.find_solution("zzzz-not-a-trained-line")
    assert "https://example.edu/a" in reply
    assert "A snippet" in reply
    assert reply.endswith("Are you satisfied with that response?")
