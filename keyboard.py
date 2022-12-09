from telebot import *

markup = types.InlineKeyboardMarkup()

all_information = types.InlineKeyboardButton('Больше информации...', callback_data='more_info')

markup.add(all_information)