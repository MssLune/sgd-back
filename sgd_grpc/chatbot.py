from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


bot = ChatBot(
    'SGD bot',
    logic_adapters=[
        'chatterbot.logic.BestMatch'
    ],
    database_uri='sqlite:///chat.sqlite3'
)

trainer = ChatterBotCorpusTrainer(bot)
trainer.train('./training/')


SGDBot = bot
