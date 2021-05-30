import os
from dotenv import load_dotenv
import telebot
from telebot import types
import ask_api

load_dotenv()

API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(func=lambda m: True)
def coinMessage(message):
  mess = message.text.lower()
  print("mess:", mess)
  resp = 'No coin for '+mess
  
  res, matchs = ask_api.matchcoin(mess)

  if res != None:
    bot.reply_to(message, ask_api.resp_mess(res))
  else:
    if len(matchs) == 0:
      bot.reply_to(message, resp)
    else:
      if len(matchs) != 0 and len(matchs) > 20:
        bot.reply_to(message, "Too much occurence: "+str(len(matchs))+" matchs\n"+"Be more specific")
      else:
        resp_match = {}
        markup = types.ReplyKeyboardMarkup()
        for match in matchs:
          resp_match["{}".format(match)] = types.KeyboardButton(match)
        for m in resp_match:
          markup.row(m)
        bot.reply_to(message, "Choose a crypto", reply_markup=markup)

def startbot():
  bot.polling()