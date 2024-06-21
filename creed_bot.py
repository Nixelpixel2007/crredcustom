import asyncio
import datetime
from telebot.async_telebot import AsyncTeleBot
import requests
import random
from bs4 import BeautifulSoup
bot = AsyncTeleBot('7031756423:AAGuq941sEubkwsqe7lDMkBQYaD1TVp19KE')
trigger_word = ['@ku1337','Ван','Вань','Ванька','Кинг','Вано','Сир','Вано','Чуня','Baня','Bаня',
                'Вaня','Ваня','Вани','Ване','Ваню','Ваней','Иван','Ивана','Ивану','Ивана','Иваном','Иване']

time_message = datetime.datetime.now()

def show():
    x =[]
    with open('words.txt', 'r') as words_txt:
        d = words_txt.read()
        for i in d.split('\n'):
            x.append(i)
    return x

def vanya_words():
    x = []
    with open('words.txt', 'r') as words_txt:
        d = words_txt.read()
        for i in d.split('\n'):
            x.append(i)
    return random.choice(x)





def roll():
    rolik= random.randint(1,100)
    return rolik


def joke():
    response =requests.get('http://anecdotica.ru/')
    soup = BeautifulSoup(response.text, 'html.parser')
    tag = soup.find('div', class_='item_text')
    return tag.get_text()

def fact():
    response = requests.get('https://randstuff.ru/fact/')
    soup = BeautifulSoup(response.text, 'html.parser')
    tag = soup.find('table', class_='text')
    return tag.get_text()


@bot.message_handler(commands=["добавить"])
async def add_word(message):
    slovo_est = False
    word = message.text.replace("/добавить ", "")
    print(message.text,message.from_user.username)
    for i in show():
        if i == word:
            slovo_est = True
    if slovo_est == False:
        with open('words.txt', 'a') as file:
            file.write(word + '\n')
        await bot.reply_to(message, f'Похвала "{word}" добавлена в список восхвалений')
    if slovo_est==True:
        await bot.reply_to(message,f'Похвала "{word}" уже существует')

@bot.message_handler(commands=['удалить'])
async def send_welcome(message):
    await bot.reply_to(message, show())


@bot.message_handler(commands=['список'])
async def send_welcome(message):
    await bot.reply_to(message, show())


@bot.message_handler(commands=['шутка'])
async def send_welcome(message):
    await bot.reply_to(message, joke())


@bot.message_handler(commands=['факт'])
async def send_welcome(message):
    await bot.reply_to(message, fact())


@bot.message_handler(commands=['roll'])
async def send_welcome(message):
    await bot.reply_to(message,roll())


@bot.message_handler(content_types=['text'])
async def echo_message(message):
    datetime_object = datetime.datetime.strptime(time_message.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
    bool_time = datetime.datetime.fromtimestamp(message.date) > datetime_object
    flag = False
    for i in trigger_word:
        for z in message.text.lower().split():  ## наверно сюда обработчик даты пихнуть
            if i.lower() == z and bool_time == True:
                flag = True
    if flag==True:
        await bot.reply_to(message,'Ваня '+vanya_words(),)
  #      print(f"Message ID: {message.message_id}")
        print(message.from_user.username)
        #print(f"{message.from_user.first_name} {message.from_user.last_name} (@{message.from_user.username})")
    #    print(f"Chat ID: {message.chat.id}")
   #     print(f"Chat Type: {message.chat.type}")

       # print(datetime.datetime.fromtimestamp(message.date))
        #print(time_message.strftime("%Y-%m-%d %H:%M:%S"))
       # print(datetime.datetime.fromtimestamp(message.date)>datetime_object)
    #    print(f"Text: {message.text}")
# Handle all other messages with content_type 'text' (content_types defaults to ['text'])

asyncio.run(bot.polling())