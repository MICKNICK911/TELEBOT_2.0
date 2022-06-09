from flask import Flask, request
import telebot
import config

secret = 12345678
bot = telebot.TeleBot(config.SECRET_KEY)
bot.set_webhook("https://telebot-2o-trial.herokuapp.com/'{}'".format(secret), max_connections=1)

app = Flask(__name__)


@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        text = update["message"]["text"]
        chat_id = update["message"]["chat"]["id"]
        bot.send_message(chat_id=chat_id, text="From the web: you said '{}'".format(text))
    return "OK"
