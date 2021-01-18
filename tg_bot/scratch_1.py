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
    print('start')
    try:
        bot.send_message(message.chat.id, "Здравствуйте, {0.first_name}! Скачивайте список проверенных партнеров по кнопке «Получить список»".format(message.from_user, bot.get_me()),
                         reply_markup=kb.button_download)
    except:
        print('error start')
        bot.send_message(114330137,
                         "Ошибка на старте была")
    #schedule_content(message.chat.id)


''' ========= END START ========= '''

''' ========= GET LIST + SEND EMAIL ============ '''


@bot.message_handler(content_types=['contact'])
def contact(message):
    try:
        cont = {'phone_number': message.contact.phone_number, 'first_name': message.contact.first_name,
                'last_name': message.contact.last_name,
                'user_id': message.contact.user_id, 'vcard': message.contact.vcard}
        print(cont)
        bot.send_message(message.chat.id, 'Спасибо, файл будет у Вас через несколько секунд')
        doc = open('partners.docx', 'rb')
        bot.send_document(message.chat.id, doc)
        bot.send_message(message.chat.id, 'По кнопке «Материалы» полезная информация бесплатно!',
                         reply_markup=kb.button_content)
        # decoded = json.loads(cont)
        df = pd.DataFrame([cont])
    except:
        print('error get list')
        bot.send_message(114330137,
                         "Ошибка на получении листа")
    try:
        dleads = pd.read_csv('leads.csv', encoding='utf-16')
        #print(df)
        if df.user_id[0] not in np.array(dleads.user_id):
            print(' ---- NEW CONTACT ----')
            dleads = pd.concat([dleads, df], axis=0)
            print(df)
            dleads.to_csv('leads.csv', index=False, encoding='utf-16')
            send_email(HOST, SUBJECT, EMAILS, FROM_ADDR, str(message.contact), PASSWORD)
    except:
        print('error email')
        bot.send_message(114330137,
                         "Ошибка на отправке имейла")


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
    )).encode('utf-8')
    #print(BODY)
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
        bot.send_message(message.chat.id, "Пожалуйста, выберите контент о компании", reply_markup=kb.callback_buttons)


@bot.callback_query_handler(func=lambda c: c.data == 'content1')
def content1(c):
    try:
        print('more_info video')
        bot.send_message(c.message.chat.id, 'Если вы экспортёр или импортёр, используйте нашу систему 14 дней бесплатно! '
                                            'Мы помогаем на каждом этапе ВЭД, все возможности смотрите в этом видео \n'
                                            'https://youtu.be/IavQvhUl9Ow',
                         reply_markup=kb.content_video_button)
    except:
        print('error video')
        bot.send_message(114330137,
                         "Ошибка на video")

@bot.callback_query_handler(func=lambda c: c.data == 'content2')
def content2(c):
    try:
        print('more_info test')
        bot.send_message(c.message.chat.id, 'Пройдите тест и узнайте, сколько стоит решить ваши задачи по ВЭД!', reply_markup=kb.content_test_button)
    except:
        print('error test')
        bot.send_message(114330137,
                         "Ошибка на test")

@bot.callback_query_handler(func=lambda c: c.data == 'content3')
def content3(c):
    try:
        print('more_info article')
        photo = open('content_photo.png', 'rb')
        bot.send_photo(c.message.chat.id, photo, caption= 'Таможенные издержки могут стоить бизнесу слишком дорого. '
                                            'Эта статья поможет вовремя обратить внимание на все подводные камни и не потерять деньги и время!',
                         reply_markup=kb.content_article_button)
    except:
        print('error article')
        bot.send_message(114330137,
                         "Ошибка на article")

@bot.callback_query_handler(func=lambda c: c.data == 'content4')
def content4(c):
    print('more_info site')
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
        bot.send_message(114330137,
                         "Ошибка сама по себе")
        pass