from chatterbot import ChatBot


class chatbot_solutions(object):
# Create a new instance of a ChatBot
    def __init__(self):
        self.bot = ChatBot(
            'Chatbot solutions',
            storage_adapter='chatterbot.storage.JsonFileStorageAdapter',
            logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch'
            },
            {
                'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                'threshold': 0.65,
                'default_response': ''
            }
        ],
            trainer='chatterbot.trainers.ListTrainer'
      )      
    # Train the chat bot with a few responses
        self.bot.train([
                'How are you?',
                'I am good.Thankyou.',
                'That is good to hear.',
                'Thank you',
                'You are welcome.',
                'Whats your name?',
                'I have no name.',
                'Where are you?',
                'I am in California.',
                'Hi',
                'Hello',
                'Hello',
        ])
        


# Get a response for some unexpected input

    def chatbot_response(self,sentence):
        response = self.bot.get_response(sentence)
        return response