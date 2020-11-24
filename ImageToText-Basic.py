# BASIC IMAGE TO TEXT BOT USING PYTESSERACT & PYTELEGRAMBOTAPI

import pytesseract as tess
import telebot
import time
import requests

bot_token = ''    # Enter your bot's token here.
bot = telebot.TeleBot(token=bot_token)


def get_text(file):

    tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text = tess.pytesseract.image_to_string(file)
    return text


def download_file(url):     # Downloading received photo

    try:
        local_filename = url.split('/')[-1]
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    except Exception:
        return "Something went wrong."
    else:
        return local_filename


@bot.message_handler(commands=['start'])
def send_welcome(message):

    bot.reply_to(message, f"*Welcome, {message.from_user.first_name}! Send /help if you are new here.*", parse_mode='Markdown')


@bot.message_handler(commands=['help'])
def send_welcome(message):

    bot.reply_to(message, '*To use this bot, just send an image containing the text.*', parse_mode='Markdown')


@bot.message_handler(content_types=['photo'])   # Checking if the received message is a photo
def at_answer(message):

    file_id = message.photo[-1].file_id     # Accessing file ID
    file_info = bot.get_file(file_id)   # Accessing file path
    url = 'https://api.telegram.org/file/bot{0}/{1}'.format(bot_token, file_info.file_path)

    bot.reply_to(message, "_Downloading file._", parse_mode='Markdown')
    file = download_file(url)

    if file != "Something went wrong.":
        bot.reply_to(message, "_File successfully downloaded._", parse_mode='Markdown')
        try:
            bot.reply_to(message, get_text(file))
        except Exception:
            bot.reply_to(message, "*Something is wrong with the image. Please try sending different image.*", parse_mode='Markdown')
    else:
        bot.reply_to(message, "*" + file + "*", parse_mode='Markdown')


while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15) 
