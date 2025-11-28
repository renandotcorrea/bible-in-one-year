from scrapper import get_today_bible_reading_url, get_profecy_cap
from message import resume_message, bible_message, profecy_message
from telegram_bot import newTelegramBot, sendBotMessage

import asyncio

def lambda_handler(event, context):
  bible_link = get_today_bible_reading_url()
  print(f'bible_link: {bible_link}')
  book_captules = get_profecy_cap(bible_link)

  telegramBot = newTelegramBot()

  resumed_message = resume_message(bible_link, book_captules)
  biblical_message = bible_message(bible_link)
  profecied_message = profecy_message(book_captules)

  # Send to Telegram Channel
  asyncio.run(sendBotMessage(telegramBot, resumed_message.replace("-", "\-").replace(".", "\.")))
  asyncio.run(sendBotMessage(telegramBot, biblical_message.replace("-", "\-").replace(".", "\.")))
  asyncio.run(sendBotMessage(telegramBot, profecied_message.replace("-", "\-").replace(".", "\.")))
