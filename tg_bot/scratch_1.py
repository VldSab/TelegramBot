import telebot
import config
import keyboard as kb
import smtplib
import json
import pandas as pd
import numpy as np

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет, {0.first_name}!".format(message.from_user, bot.get_me()), reply_markup=kb.button_download)


@bot.message_handler(content_types=['contact'])
def contact(message):
    print(message.contact)
    bot.send_message(message.chat.id, 'Спасибо, файл будет у Вас через несколько секунд')
    doc = open('output.xlsx', 'rb')
    bot.send_document(message.chat.id, doc)

    df = pd.DataFrame([message.contact])

    dleads = pd.read_csv('leads.csv', index_col=False)

    if message.contact['user_id'] not in np.array(dleads.user_id):
        dleads = pd.concat([dleads, df])
        dleads.to_csv('leads.csv', index_label=False)
        send_email(HOST, SUBJECT, EMAILS, FROM_ADDR, str(message.contact), PASSWORD)



def download(message):
    contact_button = telebot.types.KeyboardButton('Отправить контакты', request_contact=True)
    print('resr', message)
    my_keyboard = telebot.types.ReplyKeyboardMarkup([[contact_button]])  # добавляем кнопки
    return my_keyboard


def send_email(host, subject, emails, from_addr, body_text, password):
        """
        Send an email
        """

        BODY = "\r\n".join((
            "From: %s" % from_addr,
            "To: %s" % ', '.join(emails),
            "Subject: %s" % subject,
            "",
            body_text
        ))
        print(BODY)
        server = smtplib.SMTP(host, 587)
        server.starttls()
        server.login(from_addr, password)
        server.sendmail(from_addr, emails, BODY)
        server.quit()


HOST = "smtp.yandex.ru"
PASSWORD = '694768Alexis'

SUBJECT = "New lead from telegram-bot"
EMAILS = ["saberullin@condor-platform.com", 'minxerz102@hotmail.com']
FROM_ADDR = "dubinin@condor-platform.com"

bot.polling(none_stop=True)