import telebot

button_download = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    telebot.types.KeyboardButton('Получить список', request_contact=True)
)

button_content = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    telebot.types.KeyboardButton('Материалы'),
    telebot.types.KeyboardButton('Получить список', request_contact=True)
)

callback_buttons = telebot.types.InlineKeyboardMarkup().add(
    telebot.types.InlineKeyboardButton('Видео', callback_data='content1'),
    telebot.types.InlineKeyboardButton('Пройти тест', callback_data='content2'),
    telebot.types.InlineKeyboardButton('Статья', callback_data='content3'),
    telebot.types.InlineKeyboardButton('Сайт', callback_data='content4')
)

site_button = telebot.types.InlineKeyboardMarkup().add(
    telebot.types.InlineKeyboardButton('Condor', callback_data='site', url='https://www.webpilots.ru/condor')
)

content_video_button = telebot.types.InlineKeyboardMarkup().add(
    telebot.types.InlineKeyboardButton('Видео', callback_data='site', url='https://youtu.be/IavQvhUl9Ow')
)

content_test_button = telebot.types.InlineKeyboardMarkup().add(
    telebot.types.InlineKeyboardButton('Пройти тест', callback_data='site', url='https://www.webpilots.ru/condor/test')
)

content_article_button = telebot.types.InlineKeyboardMarkup().add(
    telebot.types.InlineKeyboardButton('Статья', callback_data='site', url='https://www.webpilots.ru/condor')
)
