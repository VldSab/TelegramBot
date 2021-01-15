import smtplib

import config
import keyboard as kb
import numpy as np
import pandas as pd
import telebot
import sched
import time




bot = telebot.TeleBot(config.TOKEN)
print('READY FOR WORK')

''' ========= START ============ '''


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Здравствуйте, {0.first_name}! Скачивайте список проверенных партнеров по кнопке «Получить список»".format(message.from_user, bot.get_me()),
                     reply_markup=kb.button_download)
    #schedule_content(message.chat.id)


''' ========= END START ========= '''

''' ========= GET LIST + SEND EMAIL ============ '''


@bot.message_handler(content_types=['contact'])
def contact(message):
    cont = {'phone_number': message.contact.phone_number, 'first_name': message.contact.first_name,
            'last_name': message.contact.last_name,
            'user_id': message.contact.user_id, 'vcard': message.contact.vcard}
    print(cont)
    bot.send_message(message.chat.id, 'Спасибо, файл будет у Вас через несколько секунд')
    doc = open('output.xlsx', 'rb')
    bot.send_document(message.chat.id, doc)
    bot.send_message(message.chat.id, 'По кнопке «Материалы» полезная информация бесплатно!',
                     reply_markup=kb.button_content)
    # decoded = json.loads(cont)
    df = pd.DataFrame([cont])

    dleads = pd.read_csv('leads.csv')
    # print(df)
    if df.user_id[0] not in np.array(dleads.user_id):
        print(' ---- NEW CONTACT ----')
        dleads = pd.concat([dleads, df], axis=0)
        print(dleads)
        dleads.to_csv('leads.csv', index=False)
        send_email(HOST, SUBJECT, EMAILS, FROM_ADDR, str(message.contact), PASSWORD)


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

''' ========= END GET LIST ============ '''

''' ========= MORE INFO ============ '''


@bot.message_handler(content_types=['text'])
def start_text(message):
    if message.text == "Материалы":
        print('more_info started')
        bot.send_message(message.chat.id, "Пожалйста, выберите контент о компании", reply_markup=kb.callback_buttons)


@bot.callback_query_handler(func=lambda c: c.data == 'content1')
def content1(c):
    bot.send_message(c.message.chat.id, 'Если вы экспортёр или импортёр, используйте нашу систему 14 дней бесплатно! '
                                        'Мы помогаем на каждом этапе ВЭД, все возможности смотрите в этом видео',
                     reply_markup=kb.content_video_button)

@bot.callback_query_handler(func=lambda c: c.data == 'content2')
def content2(c):
    bot.send_message(c.message.chat.id, 'Пройдите тест и узнайте сколько стоит решить ваши задачи по ВЭД!', reply_markup=kb.content_test_button)


@bot.callback_query_handler(func=lambda c: c.data == 'content3')
def content3(c):
    bot.send_message(c.message.chat.id, 'Таможенные издержки могут стоить бизнесу слишком дорого. '
                                        'Эта статья поможет вовремя обратить внимание на все подводные камни и не потерять деньги и время!',
                     reply_markup=kb.content_article_button)


@bot.callback_query_handler(func=lambda c: c.data == 'content4')
def content4(c):
    bot.send_message(c.message.chat.id, 'Сайтик зацените, он не китайский)', reply_markup=kb.site_button)


''' ========= END MORE INFO ============ '''


''' ========= SCHEDULE MESSAGE ============ '''


def send_content_1(user_id):
    print('sch cont 1')
    bot.send_message(user_id, ("отложенный контент 1, дилей 10с"))

def send_content_2(user_id):
    print('sch cont 2')
    bot.send_message(user_id, ("отложенный контент 2, дилей 5с"))

def send_content_3(user_id):
    print('sch cont 3')
    bot.send_message(user_id, ("отложенный контент 3, дилей 3с"))

def schedule_content(user_id):
    s = sched.scheduler(time.time, time.sleep)
    s.enter(delay= 10, priority=1, action = send_content_1(user_id))
    s.enter(115, 2, send_content_2(user_id))
    s.enter(18, 3, send_content_3(user_id))
    s.run(blocking = False)


''' ========= END SCHEDULE MESSAGE ============ '''

if __name__ == '__main__':
    #start_process()
    try:
        bot.polling(none_stop=True)
    except:
        pass