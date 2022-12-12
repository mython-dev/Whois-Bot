import subprocess
import sys
import os
from keyboard import *
import time
try:
    from twoip import TwoIP
    import socket
    import telebot
    import requests
except:
    print('Пожалуйста запустите: pip3 install -r requirements.txt')
    sys.exit()
    
r = requests


twoip = TwoIP(key = None)

token = '5855942888:AAFqybFV0m3_kgqCWUA1ARSV6Pk7mfc_KT0'

bot = telebot.TeleBot(token)


# Start Bot! Greeting

@bot.message_handler(commands=['start'])

def start(message):
    bot.send_message(message.chat.id, '''Привет, я помогу тебе узнать провайдера и местоположение IP-адреса или домена
    
Список команд:

/start — Перезапуск бота
/help — Отображает список основных команд
/whois — Отображает whois-информацию для IP-адреса/домена (например, /whois google.com);
/checking - Проверка существования e-mail адреса''')


# Command Help!

@bot.message_handler(commands=['help'])

def help(message):
    bot.send_message(message.chat.id, '''
    Список команд:

/start — перезапуск бота
/help — отображает список основных команд
/whois — отображает whois-информацию для IP-адреса/домена (например, /whois google.com);
/checking - Проверка существования e-mail адреса''')


# Whois 

@bot.message_handler(commands=['whois'])

def whois(message):
    global site

    if len(message.text) < 7:
        bot.send_message(message.chat.id, '''Для того чтобы проверить домен или IP достаточно отправить команду новым сообщением:
Команды:
/whois google.com

''')
        return whois
    site = message.text.split()[1:]

    try:
        # getting ip. site
        ipAddress = socket.gethostbyname(' '.join(site))
    except:
        bot.send_message(message.chat.id, 'Нет такого Домена! Попробуйте еще раз.')
        return whois
    
    try:
        provayder = twoip.provider(ip = ipAddress)
        geo = twoip.geo(ip= ipAddress)
        bot.send_message(message.chat.id, f'''
🌍IP: {ipAddress}
\nПровайдер: {provayder['name_rus']} 
Сайт провайдера: {provayder['site']}
Страна: {geo['country']}
Город: {geo['city']}
Местное время: {geo['time_zone']}''', disable_web_page_preview=True ,reply_markup=markup)
    except:
        bot.send_message(message.chat.id, 'Ваш лимит закончился, попробуйте позже!!!')



@bot.callback_query_handler(func=lambda call: True)

def more_information(call):
    if call.data == 'more_info':
        domen = ' '.join(site)
        command = (f'whois {domen}')
        info = subprocess.check_output(command, shell=True)

        bot.send_message(call.message.chat.id, 'Отправляю....')

        time.sleep(3)


        if len(info) > 4095:
            for x in range(0, len(info), 4095):
                bot.send_message(call.message.chat.id, text=info[x:x+4095], disable_web_page_preview=True)
        else:
            bot.send_message(call.message.chat.id, info, disable_web_page_preview=True)



@bot.message_handler(commands=['checking'])

def checking(message):

    if len(message.text) < 10:
        bot.send_message(message.chat.id, '''Для того чтобы проверить E-mail адрес на существования достаточно отправить команду новым сообщением:
Команды:

/checking example@gmail.com''')
        return checking

    e = message.text.split()[1:]
    email = ' '.join(e)

    try:
        api_email = r.get(f'https://api.2ip.ua/email.txt?email={email}')

        if api_email.text == 'true':
            bot.send_message(message.chat.id, f'E-mail адрес {email} существует')
        else:
            bot.send_message(message.chat.id, f'E-mail адрес {email} не существует')
    except:
        bot.send_message(message.chat.id, 'Ваш лимит закончился, попробуйте позже!!!')

@bot.message_handler(content_types=['text'])
def text(message):
    bot.send_message(message.chat.id, 'Что-то пошло нет так! нажмите на /start или /help !')

bot.polling(none_stop=True)
