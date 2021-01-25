import smtplib
from flask import Flask, request
from pymessenger.bot import Bot
from pymessenger import Element, Button
from pymessenger.user_profile import UserProfileApi
import pandas as pd
import numpy as np

app = Flask(__name__)


ACCESS_TOKEN = 'EAAF5D2xgX2IBAJ6j40A1JYYYGciFHvQ025DZBfGmwgGejgkFXuZCIgkl2Mmup7ZAUGhO7zg2PEoNtOmhQZBsk7MCxCeaeHYA8uogMTEhOsm6qkI8cSzwSuG2CGO8283JMI7kb5RJZAXM3XGmNfJEppXURWZBMl1RfuLCXDMdSx3QTl2jxVvdsc9LOQbUNvqOQZD'
VERIFY_TOKEN = 'condor1234'

bot = Bot(ACCESS_TOKEN)
print(bot)

def test_button_message(recipient_id):
    buttons = []
    button = Button(title='Получить список', type='postback', payload='get_list')
    buttons.append(button)
    text = 'Здравствуйте! Скачивайте список проверенных партнеров по кнопке «Получить список»'
    bot.send_button_message(recipient_id, text, buttons)

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


def send_email_cont(user_id, phone_number):
    s = UserProfileApi(ACCESS_TOKEN)
    user = s.get(user_id)
    user['phone_number'] = phone_number
    user.pop('profile_pic')
    df = pd.DataFrame([user])
    try:
        dleads = pd.read_csv('leads_fb.csv', encoding='utf-16')
        if int(df.id[0]) not in np.array(dleads.id):
            print(' ---- NEW CONTACT ----')
            dleads = pd.concat([dleads, df], axis=0)
            print(df)
            dleads.to_csv('leads_fb.csv', index=False, encoding='utf-16')
            send_email(HOST, SUBJECT, EMAILS, FROM_ADDR, str(user), PASSWORD)
    except:
        print('error email')
        bot.send_message(114330137,
                         "Ошибка на отправке имейла")

@app.route("/", methods=['GET', 'POST'])
def hello():
    try:
        print(request.method)
        if request.method == 'GET':
            print('GET GET GET')
            if request.args.get("hub.verify_token") == VERIFY_TOKEN:
                return request.args.get("hub.challenge")
            else:
                return 'Invalid verification token'

        if request.method == 'POST':
            output = request.get_json()
            #print('OUTPUT', output)
            event = output['entry'][0]
            #print('event', event)
            x = event['messaging'][0]
            #print('x', x)
            recipient_id = x['sender']['id']
            if recipient_id != event['id']:
                if x.get('postback'):
                    if x['postback'].get('title'):
                        message = x['postback']['title']
                        print('postback', message)
                        if message == 'Get Started':
                            test_button_message(recipient_id)

                        elif message == 'Получить список' or message == 'Список клиентов':
                            bot.send_text_message(recipient_id, 'отправьте номер')

                        elif message == "Видео":
                            buttons = [Button(title='Видео', type='web_url', url='https://youtu.be/IavQvhUl9Ow')]
                            text = 'Если вы экспортёр или импортёр, используйте нашу систему 14 дней бесплатно! Мы помогаем на каждом этапе ВЭД, все возможности смотрите в этом видео ' \
                                   'https://youtu.be/IavQvhUl9Ow'
                            bot.send_button_message(recipient_id, text, buttons)

                        elif message == "Пройти тест":
                            buttons = [Button(title='Пройти тест', type='web_url', url='https://www.webpilots.ru/condor/test')]
                            text = 'Пройдите тест и узнайте, сколько стоит решить ваши задачи по ВЭД!'
                            bot.send_button_message(recipient_id, text, buttons)

                        elif message == "Сайт":
                            buttons = [
                                Button(title='Сайт CONDOR', type='web_url', url='https://www.webpilots.ru/condor')]
                            text = 'Сайтик зацените, он не китайский)'
                            bot.send_button_message(recipient_id, text, buttons)

                        elif message == "Материалы":
                            buttons = []
                            video_but = Button(title='Видео', type='postback', payload='video')
                            buttons.append(video_but)
                            test_but = Button(title='Пройти тест', type='postback', payload='test')
                            buttons.append(test_but)
                            #article_but = Button(title='Статья', type='postback', payload='article')
                            #buttons.append(article_but)
                            site_but = Button(title='Сайт', type='postback', payload='site')
                            buttons.append(site_but)

                            text = 'Материалы о компании:'
                            bot.send_button_message(recipient_id, text, buttons)
                    else:
                        pass
                elif x.get('message'):
                    print('MESSAGE MESSAGE MESSAGE')
                    message = x['message']['text']
                    print('text', x)
                    try:
                        if int(message) > 10**10 and int(message) < 10**14:
                            buttons = [Button(title='Получить файл', type='web_url', url='https://drive.google.com/uc?export=download&id=1o9i8ng1d3AUA57tGklforl8INAiWGokX')]
                            text = 'Спасибо, файл доступен по кнопке ниже'
                            bot.send_button_message(recipient_id, text, buttons)
                            send_email_cont(x['sender']['id'], message)

                            buttons = []
                            button = Button(title='Материалы', type='postback', payload='materials')
                            buttons.append(button)
                            text = 'По кнопке «Материалы» полезная информация бесплатно!'
                            bot.send_button_message(recipient_id, text, buttons)
                    except ValueError:
                        buttons = []
                        button = Button(title='Связаться с менеджером', type='postback', payload='call_to_manager')
                        buttons.append(button)
                        text = 'Для получения доступа к списку партнеров, пожалуйста, подтвердите регистрацию, указав Ваш номер телефона.' \
                               'Если Вы хотите связаться с менеджером, нажмите на кнопку «Связаться с менеджером»'
                        bot.send_button_message(recipient_id, text, buttons)


                    #bot.send_text_message(recipient_id, message)
    except:
        pass
    return "Success"


if __name__ == "__main__":
    app.run(port=8004)