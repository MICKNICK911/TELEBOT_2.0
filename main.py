import telebot
from telebot import types
import config
import models
import functions
import time
import database
import os
from flask import Flask, request, abort
import logging

# API_TOKEN = config.SECRET_KEY
#
# WEBHOOK_HOST = 'telebot-2o-trial.herokuapp.com/'
# WEBHOOK_PORT = int(os.environ.get('PORT', 5000))
# WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr
#
# WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
# WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN,)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(config.SECRET_KEY, parse_mode=None)
app = Flask(__name__)


def main():
    # models.Base.metadata.create_all(bind=database.engine)

    start = [0]
    active_person = []
    familiar_person = []
    to_ask = []
    to_ask_source = []
    asking = []
    identifying = []
    keyword = []
    reply = []
    try_correct = []
    try_listen = []
    try_reply = []
    no_idea = []
    try_idea = []
    assure = []
    plead = []

    @bot.message_handler(func=lambda say: say.from_user)
    def reply_message(say):
        text = say.text.lower()

        if start[0] == 0:
            start.clear()
            start.append(1)

            functions.familiar(str(say.chat.id), active_person, familiar_person)

            markup = types.ReplyKeyboardMarkup(row_width=1)

            bt1 = types.KeyboardButton("TEACH ME")
            bt2 = types.KeyboardButton("CHAT WITH ME")
            markup.add(bt1, bt2)

            bot.send_sticker(chat_id=say.chat.id,
                             data="CAACAgIAAxkBAAICqGKOvt7bkApi0-0GWbyiGh4grnrWAAIdDQACHvvQSDHwOFDPb2R5JAQ")
            bot.send_message(chat_id=say.chat.id,
                             text=f"*Hello {say.chat.first_name} {say.chat.last_name}!*\nNice to meet you\nI love to learn new things",
                             parse_mode='markdown', reply_markup=markup)

        elif start[0] == 1:
            if text == "teach me":
                functions.cancel('Okay', say.chat.id, bot)
                quest = functions.ask("no idea", f'{say.chat.first_name} {say.chat.last_name}')
                if quest:
                    for items in quest:
                        to_ask.append(items['listen'])
                        to_ask_source.append(items['Author'])
                        functions.delete_excess(items['listen'], items['Author'])

                    bot.send_sticker(chat_id=say.chat.id,
                                     data="CAACAgIAAxkBAAICsGKPVqAaM9h3xzUAAUroN0oD1RMEnwACFgEAAh8BTBU10Ep_XuXSUiQE")
                    bot.send_message(chat_id=say.chat.id,
                                     text=f'Please how do I reply\n if someone say:\n *{to_ask[0].capitalize()}*',
                                     parse_mode='markdown')
                    asking.append(to_ask[0])
                    identifying.append(to_ask_source[0])
                    to_ask.remove(to_ask[0])
                    to_ask_source.remove(to_ask_source[0])
                    start.clear()
                    start.append(3)

                else:
                    bot.send_sticker(chat_id=say.chat.id,
                                     data="CAACAgIAAxkBAAICq2KPU9YhLhqVUD7gSYmUkvAfBc2WAAJZFQAC3_s4SQnqEW74KtanJAQ")
                    bot.send_message(chat_id=say.chat.id,
                                     text=f'I am listening ...',
                                     parse_mode='markdown')
                    start.clear()
                    start.append(2)

            elif text == "chat with me":
                bot.send_sticker(chat_id=say.chat.id,
                                 data="CAACAgIAAxkBAAICtGKPWr9ghbw2jru3GjGLXio0-ca2AALTEgACvfE4SB6gKvyVXsfYJAQ")
                functions.cancel('Really!\n I am flattered', say.chat.id, bot)
                start.clear()
                start.append(5)

            else:
                functions.invalid("That is wrong!\n *Press a button below*", say.chat.id, bot, say)

        elif start[0] == 2:
            keyword.clear()
            keyword.append(text)

            bot.send_sticker(chat_id=say.chat.id,
                             data="CAACAgEAAxkBAAICxWKPX5_Qoihty7wNla1iRIXKUEi_AAJGCAAC43gEAAGaajUPYa30iiQE")
            bot.send_message(chat_id=say.chat.id,
                             text="How do i reply?",
                             parse_mode='markdown')
            start.clear()
            start.append(3)

        elif start[0] == 3:
            reply.clear()
            reply.append(text)
            functions.store(asking, identifying, reply[0], asking, f"{say.chat.first_name} {say.chat.last_name}",
                            try_correct, try_reply, try_listen, keyword, reply)

            if to_ask:
                bot.send_sticker(chat_id=say.chat.id,
                                 data="CAACAgIAAxkBAAICsGKPVqAaM9h3xzUAAUroN0oD1RMEnwACFgEAAh8BTBU10Ep_XuXSUiQE")
                bot.send_message(chat_id=say.chat.id,
                                 text=f'Please how do I reply\n if someone say:\n *{to_ask[0].capitalize()}*',
                                 parse_mode='markdown')
                asking.append(to_ask[0])
                identifying.append(to_ask_source[0])
                to_ask.remove(to_ask[0])
                to_ask_source.remove(to_ask_source[0])
                start.clear()
                start.append(3)
            else:
                bot.send_sticker(chat_id=say.chat.id,
                                 data="CAACAgIAAxkBAAICyGKPgkg7YDB4MzPZesmdZv2hPBrNAAKtDAAC8ZRBSKFwPL_6H9PpJAQ")
                functions.confirm("Thanks very much\n Can you teach me more?", say.chat.id, bot)
                start.clear()
                start.append(4)

        elif start[0] == 4:
            if text == 'yes':
                bot.send_sticker(chat_id=say.chat.id,
                                 data="CAACAgIAAxkBAAIC1GKPh5FNNEPAEKvDBatZROOHoKtbAAL3DQACQcOoSAGnwNyippitJAQ")
                functions.cancel('Wow!\n you are a genius!\nI am listening ...', say.chat.id, bot)
                start.clear()
                start.append(2)

            elif text == 'no':
                start.clear()
                start.append(1)

                markup = types.ReplyKeyboardMarkup(row_width=1)

                bt1 = types.KeyboardButton("TEACH ME")
                bt2 = types.KeyboardButton("CHAT WITH ME")
                markup.add(bt1, bt2)

                bot.send_sticker(chat_id=say.chat.id,
                                 data="CAACAgIAAxkBAAICzGKPhZufSQ_8F0Y1NHE5OQnQgbhOAAJqCwACtUuoSDL_p8pk4vHmJAQ")
                bot.send_message(chat_id=say.chat.id,
                                 text=f"Thank you {say.chat.first_name} {say.chat.last_name}\nWhat can we do now?",
                                 parse_mode='markdown', reply_markup=markup)

            else:
                functions.invalid("That is wrong!\n *Press a button below*", say.chat.id, bot, say)

        elif start[0] == 5:
            send = functions.think(no_idea, try_idea, f"{say.chat.first_name} {say.chat.last_name}", text)

            if send:
                forward = send
            else:
                no_idea.clear()
                no_idea.append(1)
                find = functions.think(no_idea, try_idea, f"{say.chat.first_name} {say.chat.last_name}", text)

                if find:
                    forward = find
                else:
                    try_idea.clear()
                    try_idea.append(1)
                    finding = functions.think(no_idea, try_idea, f"{say.chat.first_name} {say.chat.last_name}", text)

                    if finding:
                        forward = finding

                        try_listen.clear()
                        try_listen.append(text)

                        assure.clear()
                        assure.append(1)
                    else:
                        forward = "no idea"
                        functions.keep(forward, text, f"{say.chat.first_name} {say.chat.last_name}")
                        plead.clear()
                        plead.append(1)
            if assure:
                try_reply.clear()
                try_reply.append(forward)

                bot.send_sticker(chat_id=say.chat.id,
                                 data="CAACAgIAAxkBAAIC5mKP8cCeTmlf5cwAASB2361S3jWStwACjw8AAnUuOUhbsCYf9OCDLyQE")
                functions.confirm(f"{forward}\n\nAm I correct?", say.chat.id, bot)

                assure.clear()
                start.clear()
                start.append(6)

            elif plead:
                markup = types.ReplyKeyboardMarkup(row_width=1)

                bt1 = types.KeyboardButton("TEACH ME")
                bt2 = types.KeyboardButton("CHAT WITH ME")
                markup.add(bt1, bt2)

                bot.send_message(chat_id=say.chat.id,
                                 text=forward,
                                 parse_mode='markdown', reply_markup=markup)
                start.clear()
                start.append(1)
                plead.clear()
            else:
                if forward == 'no idea':
                    markup = types.ReplyKeyboardMarkup(row_width=1)

                    bt1 = types.KeyboardButton("TEACH ME")
                    bt2 = types.KeyboardButton("CHAT WITH ME")
                    markup.add(bt1, bt2)

                    bot.send_message(chat_id=say.chat.id,
                                     text=forward,
                                     parse_mode='markdown', reply_markup=markup)
                    start.clear()
                    start.append(1)
                else:
                    bot.send_message(chat_id=say.chat.id, text=forward, parse_mode='markdown')

        elif start[0] == 6:
            functions.cancel('Okay', say.chat.id, bot)
            if text == 'yes':
                try_correct.clear()
                try_correct.append(1)
                print(functions.store(asking, identifying, reply, asking, f"{say.chat.first_name} {say.chat.last_name}",
                                      try_correct, try_reply, try_listen, keyword, reply))

                bot.send_sticker(chat_id=say.chat.id,
                                 data="CAACAgIAAxkBAAIC22KP5ackXekCLRO-JaM__9cGvM-UAAKaCwACsqjQSBLncOfi0EbGJAQ")
                bot.send_message(chat_id=say.chat.id, text="Thanks", parse_mode='markdown')

                start.clear()
                start.append(5)

            elif text == 'no':
                keyword.clear()
                keyword.append(try_listen[0])

                bot.send_sticker(chat_id=say.chat.id,
                                 data="CAACAgEAAxkBAAICxWKPX5_Qoihty7wNla1iRIXKUEi_AAJGCAAC43gEAAGaajUPYa30iiQE")
                bot.send_message(chat_id=say.chat.id,
                                 text="How do i reply?",
                                 parse_mode='markdown')

                start.clear()
                start.append(3)

                try_reply.clear()
                try_listen.clear()

            else:
                try_reply.clear()
                try_listen.clear()

                bot.send_sticker(chat_id=say.chat.id,
                                 data="CAACAgIAAxkBAAIC42KP8HSrKmVOreCOjuxURK0E4qVBAAKsDgACm205SDYlCZowOCzkJAQ")
                bot.send_message(chat_id=say.chat.id,
                                 text="Never mind\nI will do my research\nI am listening ...",
                                 parse_mode='markdown')

                start.clear()
                start.append(5)

    # @app.route('/' + API_TOKEN, methods=['POST'])
    # def webhook():
    #     json_string = request.stream.read().decode('utf-8')
    #     update = telebot.types.Update.de_json(json_string)
    #     bot.process_new_updates([update])
    #     print('starting')
    #     return '!', 200
    #
    #
    # @app.route('/')
    # def webhook1():
    #     bot.remove_webhook()
    #     bot.set_webhook(url='https://telebot-2o-trial.herokuapp.com/' + config.SECRET_KEY)
    #     print('ready')
    #     return '!', 200
    #
    #
    # if __name__ == '__main__':
    #     print('commencing')
    #     app.run(host=WEBHOOK_LISTEN,
    #             port=WEBHOOK_PORT,
    #             debug=True)
    bot.infinity_polling()


if __name__ == '__main__':
    bot.delete_webhook()
    main()
