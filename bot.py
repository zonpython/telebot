import telebot
import os
from flask import Flask, request
import os
print os.environ['bot_token']
print os.environ['bot_url']

# Create a telegram bot using Telegram @botfather, obtain a bot token, and put it in <BOT_TOKEN> (in my case VoloBot token)

# Create a Heroku app, using a python buildpack, and put the app name in <BOT_APP_NAME>
#(in my case it's https://volobot.herokuapp.com/bot)

# In order to get the webhook working, you should use the "Open app" button from the Heroku dashboard 

bot = telebot.TeleBot(os.environ['bot_token'])

server = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)

@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://"+os.environ['bot_url']+".herokuapp.com/bot")
    return "!", 200

server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
server = Flask(__name__)