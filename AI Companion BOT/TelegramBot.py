from collections import UserString
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from ChatGPT import ChatGPT
from DataBase import DataBase
from lang import *

class TelegramBot:
    # Инициализация бота
    def __init__(self, api_key_tg, api_keys_gpt, database_file, name_bot_command):
        self.bot = Bot(token=api_key_tg)
        self.chatgpt = ChatGPT(api_keys_gpt[0])
        self.database = DataBase(database_file)
        self.dp = Dispatcher(self.bot)
        self.name_bot_command = name_bot_command
        self.message_handler = self.dp.message_handler(commands=["start"])(self.process_start_command)

        # Запуск бота
        executor.start_polling(self.dp)

    # Функция регистрации пользователя в бд
    def RegisterUser(self, username, userid, firstname, lastname, banned=0, is_spam=1):
        try:
            userdata = self.database.query(f"SELECT * FROM users WHERE userid={userid}")
            if len(userdata) <= 0:
                self.database.query(f"INSERT INTO users (username, userid, firstname, lastname, banned, is_spam) VALUES('{username}', '{userid}', '{firstname}', '{lastname}', {banned}, {is_spam})", commit=True)
                return True
            return False
        except:
            return False

    # Функция провеки пользователя в базе данных
    def CheckUser(self, userid):
        userdata = self.database.query(f"SELECT * FROM users WHERE userid={userid}")
        if len(userdata) <= 0:
            return False
        else:
            return True

    # При нажатии на старт или отправки команды /start
    #@dp.message_handler(commands=['start'])
    async def process_start_command(self, message: types.Message):
        userid = message.from_user.id
        username = message.from_user.username
        firstname = message.from_user.first_name
        lastname = message.from_user.last_name

        # Если пользователя нету в БД, то  регистрируем его
        if(not self.CheckUser(userid)):
            self.RegisterUser(username, userid, firstname, lastname)
        await message.reply(lang['RU_COMMAND_START'].format(bot_name=self.name_bot_command))
