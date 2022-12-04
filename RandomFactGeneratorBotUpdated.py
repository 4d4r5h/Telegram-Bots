import telebot
import time
import requests
from bs4 import BeautifulSoup

# Enter your bot's token here.
bot_token = ''
bot = telebot.TeleBot(token=bot_token)


def get_random_fact():

    url = 'http://randomfactgenerator.net'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    try:
        result = soup.find('div', attrs={'id': 'z'}).text
    except Exception:
        return "Something went wrong."
    else:
        fact = result.split("\n")
        return fact[0]


@bot.message_handler(commands=['start'])
def send_welcome(message):

    bot.reply_to(
        message, f"Welcome, {message.from_user.first_name}! Send /help if you are new here.")


@bot.message_handler(commands=['help'])
def send_welcome(message):

    bot.reply_to(message, '*Everytime you send a message (except GIFs and stickers) to us, you will '
                 + 'receive a completely random fact.*', parse_mode='Markdown')


@bot.message_handler(func=lambda message: True)
def at_answer(message):

    bot.reply_to(message, "_" + get_random_fact() + "_", parse_mode='Markdown')


while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)
