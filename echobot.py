import asyncio
import datetime
import telebot
from telebot.async_telebot import AsyncTeleBot
import requests
import random
from bs4 import BeautifulSoup
import os
bot = AsyncTeleBot('7031756423:AAGuq941sEubkwsqe7lDMkBQYaD1TVp19KE')
trigger_word = ['@ku1337','Ваня,', 'Ван', 'Вань', 'Ванька', 'Кинг', 'Вано', 'Сир', 'Вано', 'Чуня', 'Baня', 'Bаня',
                'Вaня', 'Ваня', 'Вани', 'Ване', 'Ваню', 'Ваней', 'Иван', 'Ивана', 'Ивану', 'Ивана', 'Иваном', 'Иване']

time_message = datetime.datetime.now()

target_folder = 'photo'
def show():
    x = []
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
    rolik = random.randint(1, 100)
    return rolik


def joke():
    response = requests.get('http://anecdotica.ru/')
    soup = BeautifulSoup(response.text, 'html.parser')
    tag = soup.find('div', class_='item_text')
    return tag.get_text()


def fact():
    response = requests.get('https://randstuff.ru/fact/')
    soup = BeautifulSoup(response.text, 'html.parser')
    tag = soup.find('table', class_='text')
    return tag.get_text()




@bot.message_handler(content_types=["photo"])
async def save_photo(message):
    if message.caption is not None and message.caption.lower().rstrip() == '/сохранить':
        file_info = await bot.get_file(message.photo[-1].file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        with open(os.path.join(target_folder, f"saved_photo_{message.photo[-1].file_id}.jpg"), "wb") as photo:
            photo.write(downloaded_file)
        await bot.reply_to(message,f'добавлено')


@bot.message_handler(commands=["фото"])
async def send_photo(message):
    files = os.listdir('photo')
    random_file = random.choice(files)


    # Открытие файла в режиме чтения байтов
    with open(f'photo/{random_file}', 'rb') as photo:
        # Отправка фото в чат
        await bot.send_photo(message.chat.id, photo)

@bot.message_handler(commands=["добавить"])
async def add_word(message):
    len_slova = False
    if len(message.text) > 50:
        len_slova = True
    slovo_est = False
    word = message.text.replace("/добавить ", "")
    print(message.text, message.from_user.username)
    for i in show():
        if i == word:
            slovo_est = True
    if slovo_est == False and len_slova == False:
        with open('words.txt', 'a') as file:
            file.write('\n' + ' '.join(word.split()) )
        await bot.reply_to(message, f'Похвала "{" ".join(word.split())}" добавлена в список восхвалений')
    if slovo_est == True or len_slova == True:
        await bot.reply_to(message, f'Похвала "{word}" уже существует или слово слишком длинное (не более 50 символов)')



@bot.message_handler(commands=['удалить'])
async def delete(message):
    new_list = []
    del_word = message.text.replace('/удалить ','')
    slovo_est = False
    with open('words.txt', 'r') as delete:
        words = delete.read()

    for i in words.split('\n'):
        if del_word == i:
            slovo_est = True

    if slovo_est:
        g = words.replace(del_word, '')
        with open('words.txt', 'w') as delete2:
            delete2.write(g)
        with open('words.txt', 'r') as delete:
            words = delete.read()
            for i in words.split('\n'):
                print(i)
                if len(i) != 0:
                    new_list.append(i)
                    with open('words.txt', 'w') as delete2:
                        delete2.write('\n'.join(new_list))
            await bot.reply_to(message,'слово удалено')
    if not slovo_est:
        await bot.reply_to(message, 'такого слова нет')




@bot.message_handler(commands=['список'])
async def send_welcome(message):
    await bot.reply_to(message, show())


@bot.message_handler(commands=['шутка'])
async def send_welcome(message):
    await bot.reply_to(message, joke())


@bot.message_handler(commands=['факт'])
async def send_welcome(message):
    path = 'zapis/zapis.gif'
    await bot.send_animation(message.chat.id,open(path,'rb'),caption=fact())


@bot.message_handler(commands=['roll'])
async def send_welcome(message):
    await bot.reply_to(message, roll())


@bot.message_handler(content_types=['text'])
async def echo_message(message):
    datetime_object = datetime.datetime.strptime(time_message.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
    bool_time = datetime.datetime.fromtimestamp(message.date) > datetime_object
    flag = False
    for i in trigger_word:
        for z in message.text.lower().split():  ## наверно сюда обработчик даты пихнуть
            if i.lower() == z and bool_time == True:
                flag = True
    if flag == True:
        await bot.reply_to(message, 'Ваня ' + vanya_words(), )
        #      print(f"Message ID: {message.message_id}")
        print(message.from_user.username)
        # print(f"{message.from_user.first_name} {message.from_user.last_name} (@{message.from_user.username})")
    #    print(f"Chat ID: {message.chat.id}")


#     print(f"Chat Type: {message.chat.type}")

# print(datetime.datetime.fromtimestamp(message.date))
# print(time_message.strftime("%Y-%m-%d %H:%M:%S"))
# print(datetime.datetime.fromtimestamp(message.date)>datetime_object)
#    print(f"Text: {message.text}")
# Handle all other messages with content_type 'text' (content_types defaults to ['text'])

asyncio.run(bot.polling())
