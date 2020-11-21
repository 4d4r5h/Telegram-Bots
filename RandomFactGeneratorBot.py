import telebot
import time
import requests
from bs4 import BeautifulSoup

bot_token = ''    # Enter your bot's token here.
bot = telebot.TeleBot(token=bot_token)


def get_random_fact():

    url = 'https://www.generatorslist.com/random/questions/random-fact-generator'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    try:
        result = soup.find("h5", class_="card-title")
    except Exception:
        return "Something went wrong."
    else:
        fact = result.prettify().split("\n")
        return fact[1].strip()


@bot.message_handler(commands=['start'])
def send_welcome(message):

    bot.reply_to(message, f"Welcome, {message.from_user.first_name}! Send /help if you are new here.")


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