#from collections import UserString
#from aiogram import Bot, types
#from aiogram.dispatcher import Dispatcher
#from aiogram.utils import executor
#from ChatGPT import ChatGPT
#from DataBase import DataBase
from config import *
from TelegramBot import *

telegram_bot = TelegramBot(BOT_API_TOKEN, CHAT_GPT_LIST, DATABASE, NAME_BOT_COMMAND)
