#from collections import UserString
#from aiogram import Bot, types
#from aiogram.dispatcher import Dispatcher
#from aiogram.utils import executor
#from ChatGPT import ChatGPT
#from DataBase import DataBase
from config import *
from TelegramBot import *

telegram_bot = TelegramBot(BOT_API_TOKEN, CHAT_GPT_LIST, DATABASE, NAME_BOT_COMMAND)


<<<<<<< HEAD
#bot = Bot(token=BOT_API_TOKEN)
#chatgpt = ChatGPT(CHAT_API_TOKEN)
#database = DataBase(DATABASE)
#dp = Dispatcher(bot)
=======
bot = Bot(token=BOT_API_TOKEN)
chatgpt = ChatGPT(CHAT_GPT_LIST)
database = DataBase(DATABASE)
dp = Dispatcher(bot)
>>>>>>> 9c562c38209262513d70479926ebf0f6fb4f488b


## Загрузка в БД:
#def RegisterUser(username, userid, firstname, lastname, banned=0, is_spam=1):
#    userdata = database.query(f"SELECT * FROM users WHERE userid={userid}")
#    if len(userdata) <= 0:
#        database.query(f"INSERT INTO users (username, userid, firstname, lastname, banned, is_spam) VALUES('{username}', '{userid}', '{firstname}', '{lastname}', {banned}, {is_spam})", commit=True)

#def CheckUser(userid):
#    userdata = database.query(f"SELECT * FROM users WHERE userid={userid}")
#    if len(userdata) <= 0:
#        return False
#    else:
#        return True

## При нажатии на старт или отправки команды /start
#@dp.message_handler(commands=['start'])
#async def process_start_command(message: types.Message):
#    userid = message.from_user.id
#    username = message.from_user.username
#    firstname = message.from_user.first_name
#    lastname = message.from_user.last_name
#    if(not CheckUser(userid)):
#        RegisterUser(username, userid, firstname, lastname)
#    await message.reply("ChatGPT:\nПеред Вашим вопросом Вы обязательно должны ввести ключевое слово: Иванов, например: - Иванов, какие 5 фильмов сейчас популярны?'")

#@dp.message_handler(commands=['pay'])
#async def pay_command_handler(message: types.Message):
#    inline_kb = types.InlineKeyboardMarkup()
#    inline_btn = types.InlineKeyboardButton(text='Поддержать проект', url='https://www.sberbank.com/ru/person/dl/jc?linkname=au2IMrzvmC3v5kVza')
#    inline_kb.add(inline_btn)
#    await message.answer("Вы можете поддержать проект, оплатив тариф 'Плюсь' нажав на кнопку ниже.", reply_markup=inline_kb)

<<<<<<< HEAD
#users = {}
#messages = {}

##Запрос личного кабинета:
#@dp.message_handler(commands=['info'])
#async def me(message: types.Message):
#    user_id = message.from_user.id
#    if user_id not in users:
#        users[user_id] = {'balance': 10}
#    text = f"🖥 Личный кабинет пользователя:\n\n🆔 Ваш ID: {user_id};\n🙋‍♂️ Ваше имя: {message.from_user.username};\n\n💰 Осталось: {users[user_id]['balance']} токенов;"
#    await bot.send_message(chat_id=message.chat.id, text=text, reply_to_message_id=message.message_id)
=======
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    try:
        userid = message.from_user.id
        username = message.from_user.username
        firstname = message.from_user.first_name
        lastname = message.from_user.last_name
        if(not CheckUser(userid)):
            RegisterUser(username, userid, firstname, lastname)
        await message.reply("Бот работает, можете начинать общаться с ним!")
    except:
        return

@dp.message_handler(commands=['clear'])
async def process_start_command(message: types.Message):
    user_id = message.from_user.id
    CheckUser(user_id)
    #users[user_id]['chat_history'] = []
    print(f"@{message.from_user.username} Отчистил историю контекста")
    await message.reply("История контекста успешно отчищена!")
>>>>>>> 9c562c38209262513d70479926ebf0f6fb4f488b

## Очистка контекста:
#@dp.message_handler(commands=['clear'])
#async def process_clear_command(message: types.Message):
#    user_id = message.from_user.id
#    CheckUser(user_id)
#    UserString[user_id]['chat_history'] = []
#    await message.answer("История контекста успешно отчищена!")
#    print(f"@{message.from_user.username} Очистил историю контекста")

#last_request = {}

#@dp.message_handler()
#async def echo_message(message: types.Message):
#    message_id = message.message_id
#    rq = message.text
#    userid = message.from_user.id
#    username = message.from_user.username
#    firstname = message.from_user.first_name
#    lastname = message.from_user.last_name
#    if not CheckUser(userid):
#        RegisterUser(username, userid, firstname, lastname)

<<<<<<< HEAD
#    # Анимация "Печатает":
#    await bot.send_chat_action(chat_id=message.chat.id, action='typing')

#    # Если повторяется запрос:
#    if rq in last_request and last_request[rq] == userid:
#        await bot.send_message(chat_id=message.chat.id, text="Вы уже это говорили...", reply_to_message_id=message_id)
#        return
    
#    # С запросом ключевого слова "Иванов":
#    if 'Иванов' in rq or 'Иванов,' in rq:
#        generated_text = chatgpt.getAnswer(message=rq, lang="ru", temperature=0.7, max_tokens=2000)
#        await bot.send_message(chat_id=message.chat.id, text=generated_text, reply_to_message_id=message_id)
#        print(f"(@{username} -> bot): {rq}\n(bot -> @{username}): {generated_text}")

#    # Ответное сообщение пользователю на реакцию:
#    if message.text in ['Спасибо!', 'Благодарю!', 'Благодарствую!', 'Мерси!', 'Большое спасибо!', 'Спасибо большое', 'Спасибо', 'Благодарю', 'Благодарствую', 'Мерси', 'Большое спасибо', 'Спасибо большое', 'Спасибо большое,', 'Спасибо,', 'Благодарю,', 'Благодарствую,', 'Мерси,', 'Большое спасибо,', 'Спасибо за ответ', 'Спасибо за ответ!', 'Спасибо за информацию!', 'Спасибо за информацию.']:
#        if message.reply_to_message and message.reply_to_message.from_user.username:
#            recipient_username = message.reply_to_message.from_user.username
#            await bot.send_message(chat_id=message.chat.id, text=f"❤️ @{username} выразил(а) Вам благодарность!", reply_to_message_id=message.reply_to_message.message_id)

#    # Запуск бота:
#if __name__ == '__main__':
#    executor.start_polling(dp)
=======
    msg = await bot.send_message(message.from_user.id, "⏳ Бот генерирует ответ...", reply_to_message_id=message_id)
    generated_text = chatgpt.getAnswer(message=rq, lang="ru", temperature=0.7, max_tokens=1000)
    result = "";
    for key in generated_text.keys():
        result += f"\n{key} = {generated_text[key]}"
    await bot.edit_message_text(chat_id=userid, message_id=msg["message_id"], text=result)
    print(f"(@{message.from_user.username} -> bot): {rq}\n(bot -> @{message.from_user.username}): {generated_text['message']}")

if __name__ == '__main__':
    executor.start_polling(dp)
>>>>>>> 9c562c38209262513d70479926ebf0f6fb4f488b
