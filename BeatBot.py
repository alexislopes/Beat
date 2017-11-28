import datetime
import re
import telebot
import time
import emoji
import unicodedata
import mysql.connector
from mysql.connector import errorcode
from telebot import types
import random


bot = telebot.TeleBot("BOT TOKEN")

address = "CARD ADDRESS"

markup = types.InlineKeyboardMarkup()
g = types.InlineKeyboardButton('Adicione-me a um grupo', url='https://telegram.me/PrototypeBot?startgroup=0')
markup.add(g)

intro = ['Para uma melhor experiencia adicione-me a grupos', 'Será mais divertido se você me adicionar a algum grupo',
         'Meus algoritmos foram escritos para que eu apenas funcione em grupos']



################################### IT DOES A QUERY TO GET ALL THE KEY WORDS FROM DB ###################################


def key_words():  # verificar se funciona com o filterString
    print("\ni'm in key_words.")

    keywordslist = []
    query = "SELECT palavraChave FROM cards"
    cursor.execute(query)

    for keyword in cursor:
        keyword = str(keyword)
        keyword.rpartition("'")
        keyword = keyword[2:-3]
        keywordslist.append(keyword)

    return keywordslist


##################################### IT DOES A QUERY TO GET ALL ID USERS FROM DB ######################################

userslist = []


def users():
    print("\n i'm in users.")
    query = "SELECT id FROM users"
    cursor.execute(query)

    for user in cursor:
        user = str(user)
        user = filter_string(user)
        user = int(user)
        userslist.append(user)

    return userslist


############################################ IT GETS ALL CARDS FROM AN USER ############################################


def get_cardids(nickname, cardid):
    print("\n i'm in get_cards.")

    table = nickname + 'deck'
    query = "SELECT cardid FROM {}".format(table)
    cursor.execute(query)

    ids = []

    for id in cursor:
        id = str(id)
        id = filter_string(id)
        id = int(id)
        ids.append(id)

    print(ids)
    if cardid in ids:
        print('{} is in list'.format(cardid))
        return True
    else:
        print('{} is not in list'.format(cardid))
        return False


####################### IT DOES A QUERY TO GET THE ARCHIEVE NAME THAT MATCHES WITH THE KEY WORD ########################


def send_card(chatid, nickname, key, name):
    print("\n i'm in send_card.")
    global address


    query = "SELECT id, nome, nomeArquivo FROM cards WHERE palavraChave = '{}'".format(key)
    cursor.execute(query)

    for cardid, cardname, file in cursor:
        cardid = str(cardid)
        cardid = filter_string(cardid)
        cardid = int(cardid)
        isinlist = get_cardids(nickname, cardid)
        if not isinlist:
            file = str(file)
            card = open(address + file, 'rb')
            bot.send_photo(chatid, card, 'Boa {}! \nO card "{}" foi desbloqueado!'.format(name, cardname))
            store_card(cardid, nickname, cardname, file)
            print('The file {} was sent to {}!'.format(file, nickname))


################################ IT FILTERS THE STRING TAKING OFF ACCENTS AND PUNCTUATION ##############################

def filter_string(string):
    print("\n i'm in filter_string.")

    l = unicodedata.normalize('NFKD', string)
    newstring = u"".join([c for c in l if not unicodedata.combining(c)])
    substring = re.sub('[^a-zA-Z0-9 \\\]', '', newstring)

    return substring.lower()


################################### IT CHECKS THE STRING TRYING TO FIND A KEY WORD #####################################

def find_key_word(chatid, user, message, nameuser):
    print("\n i'm in find_key_word.")

    message = filter_string(message)
    message = message.split(' ')
    count = 0
    for word in message:
        count += 1
        if word in currentkeywords:
            key = message[count - 1]
            send_card(chatid, user, key, nameuser)
            break
        else:
            continue


##################################### IT CHECKS IF THE USER IS ALREADY IN THE LIST #####################################


def verify_user(userid):
    print("\n i'm in verify_users.")

    if userid in userslist:
        print('is an user')
        return True
    else:
        print('is not an user')
        return False


######################################### IT REGISTERS THE NEW USER IN THE DB ##########################################


def add_user(userid, nickname, nameuser):
    print("\n i'm in add_users.")

    day = datetime.date.today()
    query = "INSERT INTO users(id, nome, username, joinday) VALUES ('{}', '{}', '{}', '{}')".format(userid, nameuser,
                                                                                                    nickname, day)
    try:
        cursor.execute(query)
    except mysql.connector.Error as err:
        print(err.msg)


############################## IT CREATES A TABLE TO STORE USERS CARDS WITH AN UNIQUE NAME #############################


def table_creator(nickname, name):
    print("\n i'm in table_creator.")
    nickname = str(nickname).lower().strip()
    name = str(name).lower().strip(' ')
    print(name)
    print(nickname)

    if nickname != 'none':
        table = nickname + "deck"
    else:
        table = name + 'deck'



    query = "CREATE TABLE `{}` (" \
            "  `cardid` int NOT NULL," \
            "  `cardname` varchar(40) NOT NULL," \
            "  `card` varchar(40)," \
            "  `unlockday` date," \
            "  `unlocktime` time," \
            "  PRIMARY KEY (`cardid`)" \
            ") ENGINE=InnoDB".format(table)

    try:
        print("Creating table {}: ".format(table), end='')
        cursor.execute(query)
    except mysql.connector.Error as er:
        if er.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(er.msg)
    else:
        print("OK")


#################################### IT GETS INFORMATION'S CHAT FROM THE MESSAGE  ######################################


def get_chat_info(message):
    chatinfo = {'id': '', 'type': '', 'title': ''}

    chattypo = message.chat.type
    chatinfo['typo'] = chattypo

    chatid = message.chat.id
    chatinfo['id'] = chatid

    chattitle = message.chat.title
    chatinfo['title'] = chattitle

    return chatinfo


#################################### IT GETS INFORMATION'S USER FROM THE MESSAGE  ######################################


def get_user_info(message):
    userinfo = {'id': '', 'name': '', 'nickname': ''}

    userid = message.from_user.id
    userinfo['id'] = userid

    nickname = message.from_user.username
    userinfo['nickname'] = nickname

    name = message.from_user.first_name + ' ' + message.from_user.last_name
    userinfo['name'] = name

    isuser = verify_user(userid)

    if not isuser:
        add_user(userid, nickname, name)
        table_creator(nickname, name)

    return userinfo


################################## IT STRORES THE CARD IN THE RESPECTIVE USER TABLE  ###################################


def store_card(cardid, nickname, cardname, file):
    print("\n i'm in store_card.")

    day = datetime.date.today()
    time = str(datetime.datetime.today().time())
    time.strip(':')
    time = time[0:5]
    table = nickname + "deck"
    query = "INSERT INTO {}(" \
            "cardid, cardname, card, unlockday, unlocktime) " \
            "VALUES ('{}', '{}', '{}', '{}', '{}')".format(table, cardid, cardname, file, day, time)

    try:
        cursor.execute(query)
        cnx.commit()
        print('card was stored in {}'.format(table))
    except mysql.connector.Error as err:
        print(err)


#################################### IT FORMATS DATE AND TIME TO BE SENT CORRECTLY #####################################


def format_datetime(date, time):

    datetime = {'date': '', 'time': ''}

    date = str(date).split('-')
    date = '{}/{}/{}'.format(date[2], date[1], date[0])
    datetime['date'] = date

    time = str(time).split(':')
    time = '{}:{}'.format(time[0], time[1])
    datetime['time'] = time

    return datetime

################################### IT HANDLES ALL MESSAGES WITH THE /MYDECK COMMAND ###################################


@bot.message_handler(commands=['mydeck'])
def my_deck(message):
    global address
    print("\n i'm in my_deck.")
    uinfos = get_user_info(message)
    cinfos = get_chat_info(message)

    if start:
        cursorbuff = cnx.cursor(buffered=True)

        table = uinfos['nickname'] + "deck"
        query = "SELECT cardname, card, unlockday, unlocktime FROM {}".format(table)

        if cinfos['typo'] == 'group':
            try:
                cursorbuff.execute(query)

                if cursorbuff.rowcount == 0:
                    bot.send_message(cinfos['id'], "Poxa {} parece que seu deck está vazio. Mas continue conversando, "
                                                   "que só assim elas serão desbloqueadas.".format(uinfos['name']))

                else:
                    bot.send_message(cinfos['id'], "Aqui está seu deck {}:".format(uinfos['name']))
                    for name, file, unlockday, unlocktime in cursorbuff:
                        datetime = format_datetime(unlockday, unlocktime)
                        card = open(address + file, 'rb')
                        bot.send_photo(cinfos['id'], card, '{} \nDesbloqueada em: {} ás {}'.format(name, datetime['date'], datetime['time']))

            except mysql.connector.Error as er:
                print(er)
        else:
            bot.send_message(cinfos['id'], random.choice(intro), reply_markup=markup)
    else:
        bot.send_message(cinfos['id'], 'Primeiro você precisa usar o camando /start.')


################################### IT HANDLES ALL MESSAGES WITH THE /START COMMAND ####################################


@bot.message_handler(commands=['start'])
def send_start(message):
    global start, markup
    start = True
    uinfos = get_user_info(message)
    cinfos = get_chat_info(message)

    if cinfos['typo'] == 'private':
        bot.send_message(cinfos['id'], 'Olá, para uma melhor experiência, adicione-me a grupos.', reply_markup=markup)

    else:
        bot.send_message(cinfos['id'], 'Saudações pessoas do {}.\nVamos colecionar cartas!'.format(cinfos['title']))


################################### IT HANDLES ALL MESSAGES WITH THE /HELP COMMAND #####################################


@bot.message_handler(commands=['help'])
def send_help(message):
    print("\n i'm in send_help.")


############################ IT HANDLES ALL MESSAGES WITHOUT THE /START OR /HELP COMMAND ###############################


@bot.message_handler(func=lambda message: True, content_types=['text'])
def all_mesages(message):
    users()
    print(str(message))
    global markup, intro
    uinfos = get_user_info(message)
    cinfos = get_chat_info(message)

    if start:
        print("\n i'm in all_messages.")
        message = str(message)
        if cinfos['typo'] == 'private':
            bot.send_message(cinfos['id'], random.choice(intro), reply_markup=markup)

        else:
            find_key_word(cinfos['id'], uinfos['nickname'], message, uinfos['name'])
    else:
        bot.send_message(cinfos['id'], 'Primeiro você precisa usar o comando /start.')

########################################## IT TRIES A CONNECTION WITH THE DB ###########################################


try:
    cnx = mysql.connector.connect(user='root', database='deck')
    print('successfully connected with the {} database'.format(cnx.database))

    cursor = cnx.cursor()
    users()
    currentkeywords = key_words()
    start = False
    bot.polling()


except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cnx.close()
