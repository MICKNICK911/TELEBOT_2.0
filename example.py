from flask import Flask, request
import telebot
import config

bot = telebot.TeleBot(config.SECRET_KEY)
bot.remove_webhook()
bot.set_webhook(url='https://telebot-2o-trial.herokuapp.com/' + config.SECRET_KEY, max_connections=1)

app = Flask(__name__)


@app.route('/' + config.SECRET_KEY, methods=['POST'])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        text = update["message"]["text"]
        chat_id = update["message"]["chat"]["id"]
        bot.send_message(chat_id, f"From the web: you said '{text}'")
    return "OK"
