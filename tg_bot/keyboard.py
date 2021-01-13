import telebot

# button_download = telebot.types.KeyboardButton('get list')

# greet_kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
# greet_kb.add(button_download)

# greet_kb1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add(button_download)

button_download = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    telebot.types.KeyboardButton('get list', request_contact=True)
)

button_content = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    telebot.types.KeyboardButton('more info'),
    telebot.types.KeyboardButton('get list', request_contact=True)
)

callback_buttons = telebot.types.InlineKeyboardMarkup().add(
    telebot.types.InlineKeyboardButton('conten 1', callback_data='content1'),
    telebot.types.InlineKeyboardButton('conten 2', callback_data='content2'),
    telebot.types.InlineKeyboardButton('conten 3', callback_data='content3')

)

site_button = telebot.types.InlineKeyboardMarkup().add(
    telebot.types.InlineKeyboardButton('Condor', callback_data='site', url='https://www.webpilots.ru/condor')
)
