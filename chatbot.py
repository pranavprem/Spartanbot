from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import logging
#from chatterbot.trainers import ChatterBotCorpusTrainer

bot = ChatBot('Foram')

bot = ChatBot(
    'Foram',
    storage_adapter='chatterbot.storage.JsonFileStorageAdapter',
    logic_adapters=[
        "chatterbot.logic.MathematicalEvaluation",
#        "chatterbot.logic.TimeLogicAdapter",
        "chatterbot.logic.BestMatch"
    ],
    input_adapter='chatterbot.input.TerminalAdapter',
    output_adapter='chatterbot.output.TerminalAdapter',
    database='./database.json'
)

bot.set_trainer(ListTrainer)
#bot.set_trainer(ChatterBotCorpusTrainer)



bot.train([
    'How are you?',
    'I am good.Thankyou.',
    'That is good to hear.',
    'Thank you',
    'You are welcome.',
    'Hi',
    'Hello',
    'Whats your name?',
    'I have no name.',
    'Where are you?',
    'I am in California.'
])


while True:
    try:
     response = bot.get_response(None)

    except(KeyboardInterrupt, EOFError, SystemExit):
        break


