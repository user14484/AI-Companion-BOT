from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from ChatGPT import ChatGPT
from DataBase import DataBase

from config import *


bot = Bot(token=BOT_API_TOKEN)
chatgpt = ChatGPT(CHAT_GPT_LIST)
database = DataBase(DATABASE)
dp = Dispatcher(bot)



def RegisterUser(username, userid, firstname, lastname, banned=0, is_spam=1):
    userdata = database.query(f"SELECT * FROM users WHERE userid={userid}")
    if len(userdata) <= 0:
        database.query(f"INSERT INTO users (username, userid, firstname, lastname, banned, is_spam) VALUES('{username}', '{userid}', '{firstname}', '{lastname}', {banned}, {is_spam})", commit=True)

def CheckUser(userid):
    userdata = database.query(f"SELECT * FROM users WHERE userid={userid}")
    if len(userdata) <= 0:
        return False
    else:
        return True


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



@dp.message_handler()
async def echo_message(message: types.Message):
    message_id = message.message_id
    rq = message.text
    userid = message.from_user.id
    username = message.from_user.username
    firstname = message.from_user.first_name
    lastname = message.from_user.last_name
    if(not CheckUser(userid)):
        RegisterUser(username, userid, firstname, lastname)

    msg = await bot.send_message(message.from_user.id, "⏳ Бот генерирует ответ...", reply_to_message_id=message_id)
    generated_text = chatgpt.getAnswer(message=rq, lang="ru", temperature=0.7, max_tokens=1000)
    result = "";
    for key in generated_text.keys():
        result += f"\n{key} = {generated_text[key]}"
    await bot.edit_message_text(chat_id=userid, message_id=msg["message_id"], text=result)
    print(f"(@{message.from_user.username} -> bot): {rq}\n(bot -> @{message.from_user.username}): {generated_text['message']}")

if __name__ == '__main__':
    executor.start_polling(dp)
