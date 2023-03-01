<<<<<<< HEAD
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
        self.chatgpt = ChatGPT(api_keys_gpt)
        self.database = DataBase(database_file)
        self.dp = Dispatcher(self.bot)
        self.name_bot_command = name_bot_command


        self.dp.message_handler(commands=["start"])(self.process_start_command)
        self.dp.message_handler(commands=["pay"])(self.pay_command_handler)
        self.dp.message_handler(commands=["info"])(self.info_command_handler)
        self.dp.message_handler(commands=["admin"])(self.admin_command_handler)
        self.dp.message_handler(commands=["test"])(self.test_command_handler)
        self.dp.message_handler()(self.echo_message)
        self.dp.callback_query_handler(lambda call: call.data == 'admin_give_money')(self.admin_give_money)
        self.dp.callback_query_handler(lambda call: call.data == 'admin_add_tokens')(self.admin_add_tokens)

        # Запуск бота
        executor.start_polling(self.dp)

    # Функция регистрации пользователя в бд
    def RegisterUser(self, username, userid, firstname, lastname, banned=0, is_spam=1, balance=0, lang='ru', tokens=500):
        try:
            userdata = self.database.query(f"SELECT * FROM users WHERE userid='{userid}'")
            if len(userdata) <= 0:
                self.database.query(f"INSERT INTO users (username, userid, firstname, lastname, banned, is_spam) VALUES('{username}', '{userid}', '{firstname}', '{lastname}', {banned}, {is_spam})", commit=True)
                self.database.query(f"INSERT INTO settings (userid, balance, lang, tokens) VALUES('{userid}', {balance}, '{lang}', {tokens})", commit=True)
                return True
            return False
        except:
            return False

    # Функция провеки пользователя в базе данных
    def CheckUser(self, userid):
        userdata = self.database.query(f"SELECT * FROM users WHERE userid='{userid}'")
        if len(userdata) <= 0:
            return False
        else:
            return True

    # Функция проверки и вычитания токенов
    def CheckTokens(self, userid, text):
        userdata = self.database.query(f"SELECT * FROM settings WHERE userid='{userid}'")
        
        tokens = text.split()
        num_tokens = len(tokens)

        if(num_tokens > userdata["tokens"]):
            return False
        
        self.database.query(f"UPDATE settings SET tokens={int(userdata['tokens']) - num_tokens} WHERE userid='{userid}'", commit=True)
        return True
    
    # При нажатии на старт или отправки команды /start
    async def process_start_command(self, message: types.Message):
        userid = message.from_user.id
        username = message.from_user.username
        firstname = message.from_user.first_name
        lastname = message.from_user.last_name

        # Если пользователя нету в БД, то  регистрируем его
        if(not self.CheckUser(userid)):
            self.RegisterUser(username, userid, firstname, lastname)
        await message.reply(lang['RU_COMMAND_START'].format(bot_name=self.name_bot_command))

    # Функция ответа на команду /pay
    async def pay_command_handler(self, message: types.Message):
        inline_kb = types.InlineKeyboardMarkup()
        inline_btn = types.InlineKeyboardButton(text='Поддержать проект', url='https://www.sberbank.com/')
        inline_kb.add(inline_btn)
        await message.answer("Вы можете поддержать проект, оплатив тариф 'Плюс' нажав на кнопку ниже.", reply_markup=inline_kb)

    def GetUserSettings(self, userid):
        userdata = self.database.query(f"SELECT * FROM settings WHERE userid={userid}")
        if len(userdata) <= 0:
            return {"result": userdata, "error": False}
        else:
            return {"result": userdata, "error": True}

    # Функция ответа на команду /info
    async def info_command_handler(self, message: types.Message):
        user_id = message.from_user.id
        settings_user = self.GetUserSettings(user_id)

        if(settings_user["error"]):
            settings_user = settings_user["result"]
        else:
            return

        balance = settings_user["balance"]
        lang = settings_user["lang"]
        tokens = settings_user["tokens"]
        text = f"🖥 Личный кабинет пользователя:\n\n🆔 Ваш ID: {user_id};\n🙋‍♂️ Ваше имя: {message.from_user.username};\n\n💰 Осталось: {balance}₽ ~ {tokens} токенов;"
        await self.bot.send_message(chat_id=message.chat.id, text=text, reply_to_message_id=message.message_id)

    # Функция ответа на сообщение
    async def echo_message(self, message: types.Message):
        message_id = message.message_id
        rq = message.text
        userid = message.from_user.id
        username = message.from_user.username
        firstname = message.from_user.first_name
        lastname = message.from_user.last_name
        if not self.CheckUser(userid):
            self.RegisterUser(username, userid, firstname, lastname)

        me = await self.bot.get_me()

        # Ответное сообщение пользователю на реакцию:
        if rq in ['Спасибо!', 'Благодарю!', 'Благодарствую!', 'Мерси!', 'Большое спасибо!', 'Спасибо большое', 'Спасибо', 'Благодарю', 'Благодарствую', 'Мерси', 'Большое спасибо', 'Спасибо большое', 'Спасибо большое,', 'Спасибо,', 'Благодарю,', 'Благодарствую,', 'Мерси,', 'Большое спасибо,', 'Спасибо за ответ', 'Спасибо за ответ!', 'Спасибо за информацию!', 'Спасибо за информацию.']:
            if message.reply_to_message and message.reply_to_message.from_user.username:
                #recipient_username = message.reply_to_message.from_user.username
                await self.bot.send_message(chat_id=message.chat.id, text=f"❤️ @{me.username} выразил(а) Вам благодарность!", reply_to_message_id=message.reply_to_message.message_id)
                print(f"(@{username} -> bot): {rq}\n(bot -> @{username}): ❤️ @{me.username} выразил(а) Вам благодарность!")
                return

        # Анимация "Печатает":
        await self.bot.send_chat_action(chat_id=message.chat.id, action='typing')
    
        # С запросом ключевого слова "Иванов":
        if self.name_bot_command in rq or f'{self.name_bot_command},' in rq:
            if(self.CheckTokens(userid, rq)):
                generated_text = self.chatgpt.getAnswer(message=rq, lang="ru", temperature=0.7, max_tokens=1000)
                await self.bot.send_message(chat_id=message.chat.id, text=generated_text["message"], reply_to_message_id=message_id)
                print(f"(@{username} -> bot): {rq}\n(bot -> @{username}): {generated_text['message']}")
            else:
                await self.bot.send_message(chat_id=message.chat.id, text="У вас не достаточно токенов. Пожалуйста пополните свой баланс!", reply_to_message_id=message_id)
                print(f"(@{username} -> bot): {rq}\n(bot -> @{username}): У вас не достаточно токенов. Пожалуйста пополните свой баланс!")


    def is_user_admin(self, user_id):
        try:
            userdata = self.database.query(f"SELECT * FROM users WHERE userid={user_id}")
            if len(userdata) > 0 and userdata['admin'] == 1:
                return True
            return False
        except:
            return False

    # При нажатии на старт или отправки команды /test
    async def test_command_handler(self, message: types.Message):
        message_id = message.message_id
        rq = message.text
        userid = message.from_user.id
        username = message.from_user.username
        firstname = message.from_user.first_name
        lastname = message.from_user.last_name

        user, money = message.get_args().split()

        # Если пользователя нету в БД, то  регистрируем его
        if(not self.CheckUser(userid)):
            self.RegisterUser(username, userid, firstname, lastname)
        await self.bot.send_message(chat_id=message.chat.id, text=f"user = {user}\nmoney = {money}", reply_to_message_id=message_id)

    # При нажатии на старт или отправки команды /admin
    async def admin_command_handler(self, message: types.Message):
        message_id = message.message_id
        rq = message.text
        userid = message.from_user.id
        username = message.from_user.username
        firstname = message.from_user.first_name
        lastname = message.from_user.last_name

        # Если пользователя нету в БД, то  регистрируем его
        if(not self.CheckUser(userid)):
            self.RegisterUser(username, userid, firstname, lastname)
        await self.bot.send_message(chat_id=message.chat.id, text="Выберете действие:", reply_to_message_id=message_id, reply_markup=self.admin_buttons())

    # Кнопки админки
    def admin_buttons(self):
        buttons = types.InlineKeyboardMarkup(row_width=2)
        buttons.add(
            types.InlineKeyboardButton(text="Выдать деньги", callback_data='admin_give_money'),
            types.InlineKeyboardButton(text="Выдать токены", callback_data='admin_add_tokens')
            )
        buttons.row(
            types.InlineKeyboardButton(text="Рассылка", callback_data='admin_spam')
            )
        buttons.row(
            types.InlineKeyboardButton(text="Забанить", callback_data='admin_ban')
            )
        return buttons

    # Функция по выдаче денег
    async def admin_give_money(self, call: types.CallbackQuery):
        await self.bot.send_message(chat_id=call.message.chat.id, text="Введите формате: <code>/money @username количество</code>", parse_mode='HTML')

    # Функция по выдаче денег
    async def admin_add_tokens(self, call: types.CallbackQuery):
        await self.bot.send_message(chat_id=call.message.chat.id, text="Введите формате: <code>/money @username количество</code>", parse_mode='HTML')
=======
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
        self.chatgpt = ChatGPT(api_keys_gpt)
        self.database = DataBase(database_file)
        self.dp = Dispatcher(self.bot)
        self.name_bot_command = name_bot_command


        self.dp.message_handler(commands=["start"])(self.process_start_command)
        self.dp.message_handler(commands=["pay"])(self.pay_command_handler)
        self.dp.message_handler(commands=["info"])(self.info_command_handler)
        self.dp.message_handler()(self.echo_message)

        # Запуск бота
        executor.start_polling(self.dp)

    # Функция регистрации пользователя в бд
    def RegisterUser(self, username, userid, firstname, lastname, banned=0, is_spam=1, balance=0, lang='ru', tokens=0):
        try:
            userdata = self.database.query(f"SELECT * FROM users WHERE userid={userid}")
            if len(userdata) <= 0:
                self.database.query(f"INSERT INTO users (username, userid, firstname, lastname, banned, is_spam) VALUES('{username}', '{userid}', '{firstname}', '{lastname}', {banned}, {is_spam})", commit=True)
                self.database.query(f"INSERT INTO settings (userid, balance, lang, tokens) VALUES('{userid}', {balance}, '{lang}', {tokens})", commit=True)
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
    async def process_start_command(self, message: types.Message):
        userid = message.from_user.id
        username = message.from_user.username
        firstname = message.from_user.first_name
        lastname = message.from_user.last_name

        # Если пользователя нету в БД, то  регистрируем его
        if(not self.CheckUser(userid)):
            self.RegisterUser(username, userid, firstname, lastname)
        await message.reply(lang['RU_COMMAND_START'].format(bot_name=self.name_bot_command))

    # Функция ответа на команду /pay
    async def pay_command_handler(self, message: types.Message):
        inline_kb = types.InlineKeyboardMarkup()
        inline_btn = types.InlineKeyboardButton(text='Поддержать проект', url='https://www.sberbank.com/')
        inline_kb.add(inline_btn)
        await message.answer("Вы можете поддержать проект, оплатив тариф 'Плюс' нажав на кнопку ниже.", reply_markup=inline_kb)

    def GetUserSettings(self, userid):
        userdata = self.database.query(f"SELECT * FROM settings WHERE userid={userid}")
        if len(userdata) <= 0:
            return {"result": userdata, "error": False}
        else:
            return {"result": userdata, "error": True}

    # Функция ответа на команду /info
    async def info_command_handler(self, message: types.Message):
        user_id = message.from_user.id
        settings_user = self.GetUserSettings(user_id)

        if(settings_user["error"]):
            settings_user = settings_user["result"]

        balance = settings_user["balance"]
        lang = settings_user["lang"]
        tokens = settings_user["tokens"]
        text = f"🖥 Личный кабинет пользователя:\n\n🆔 Ваш ID: {user_id};\n🙋‍♂️ Ваше имя: {message.from_user.username};\n\n💰 Осталось: {balance}₽ ~ {tokens} токенов;"
        await self.bot.send_message(chat_id=message.chat.id, text=text, reply_to_message_id=message.message_id)

    # Функция ответа на сообщение
    async def echo_message(self, message: types.Message):
        message_id = message.message_id
        rq = message.text
        userid = message.from_user.id
        username = message.from_user.username
        firstname = message.from_user.first_name
        lastname = message.from_user.last_name
        if not self.CheckUser(userid):
            self.RegisterUser(username, userid, firstname, lastname)

        #me = self.bot.get_me()
        #print(me.username)

        ## Ответное сообщение пользователю на реакцию:
        #if rq in ['Спасибо!', 'Благодарю!', 'Благодарствую!', 'Мерси!', 'Большое спасибо!', 'Спасибо большое', 'Спасибо', 'Благодарю', 'Благодарствую', 'Мерси', 'Большое спасибо', 'Спасибо большое', 'Спасибо большое,', 'Спасибо,', 'Благодарю,', 'Благодарствую,', 'Мерси,', 'Большое спасибо,', 'Спасибо за ответ', 'Спасибо за ответ!', 'Спасибо за информацию!', 'Спасибо за информацию.']:
        #    if message.reply_to_message and message.reply_to_message.from_user.username:
        #        #recipient_username = message.reply_to_message.from_user.username
        #        await self.bot.send_message(chat_id=message.chat.id, text=f"❤️ @{me.username} выразил(а) Вам благодарность!", reply_to_message_id=message.reply_to_message.message_id)
        #        #print(f"(@{username} -> bot): {rq}\n(bot -> @{username}): ❤️ @{me.username} выразил(а) Вам благодарность!")
        #        return

        # Анимация "Печатает":
        await self.bot.send_chat_action(chat_id=message.chat.id, action='typing')
    
        # С запросом ключевого слова "Иванов":
        if self.name_bot_command in rq or f'{self.name_bot_command},' in rq:
            generated_text = self.chatgpt.getAnswer(message=rq, lang="ru", temperature=0.7, max_tokens=1000)
            await self.bot.send_message(chat_id=message.chat.id, text=generated_text["message"], reply_to_message_id=message_id)
            print(f"(@{username} -> bot): {rq}\n(bot -> @{username}): {generated_text['message']}")

>>>>>>> 60f5596e1a6ef75abf3adb3d0dc125e0aa6b11db
