import telebot

#button_download = telebot.types.KeyboardButton('get list')

#greet_kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
#greet_kb.add(button_download)

#greet_kb1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add(button_download)

button_download = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    telebot.types.KeyboardButton('get list', request_contact=True)
)