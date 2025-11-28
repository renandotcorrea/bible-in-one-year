import telegram
import os
from dotenv import load_dotenv

load_dotenv()

def newTelegramBot():
  return telegram.Bot(os.getenv("BOT_TOKEN"))

async def sendBotMessage(bot, message):
  async with bot:
    await bot.send_message(text=message, chat_id=os.getenv("CHAT_ID"), parse_mode="MarkdownV2")