###########################################################################
###########################################################################
###                                                                     ###
###                 Jaybiz Music Bot For Telegram v1.0                  ###
###                      © Coded by DrCodee 2020                        ###
###                       Instagram.com/DrCodee                         ###
###       Telegram Channel  https://t.me/DrCodee  کانال تلگرام         ###
###    You can contact me for suggestions, fixes or any questions ;)    ###
###                                                                     ###
###########################################################################
###########################################################################

import telebot
import re
from telebot import apihelper
from telebot import types
import mysql.connector
from mysql.connector import errorcode

# با فعال کردن گزینه ی زیر می تونین برای بات پروکسی تعریف کنین و ربات توسط پروسکی به سرور تلگرام متصل می شود
# enabling this option allows you to use proxy for your bot connection

# apihelper.proxy = {'https':'https://userproxy:password@proxy_address:port'} 

# زبان های موجود فارسی و انگلیسی
#  Available languages: FA (Farsi), EN (English)
language = "FA"

# توکن ربات خود را اینجا وارد کنید
# Paste your bot token here!
token = 'YOURTOKEN'
bot = telebot.TeleBot(token)

# این قسمت مشخصات دیتابیس رو وارد کنید
# Fill this part with your MySQL database information
DB_NAME = 'database'
mydb = mysql.connector.connect(
    host="host",
    user="username",
    passwd="password",
)

cursor = mydb.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

try:
    print("Creating tables..")
    cursor.execute(
        "CREATE TABLE savedmusic (`ID` VARCHAR(255), `FILEID` VARCHAR(255), `DURATION` VARCHAR(255), `PERFORMER` VARCHAR(255), `TITLE` VARCHAR(255))")
    cursor.execute(
        "CREATE TABLE userinfo (`ID` VARCHAR(255), `STEP` INT NOT NULL)")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print("Tables already exists!")
    else:
        print(err.msg)
else:
    print("Tables created!")

def goHomePage(chatid, type):
    cursor.execute("UPDATE `userinfo` SET `STEP` = '" + str(0) + "' WHERE `ID` = '" + str(chatid) + "'")
    mydb.commit()
    if type == 0:
        if(language == "FA"):
            startmarkup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
            itembtn1 = types.KeyboardButton('📍کانال تلگرام')
            itembtn2 = types.KeyboardButton('📣تبلیغات')
            itembtn3 = types.KeyboardButton('☎️پشتیبانی')
            startmarkup.add(itembtn1, itembtn2, itembtn3)
            bot.send_message(chatid, "سلام من ربات موزیکم، می تونی آهنگ مورد علاقتو به صورت زیر سرچ و پیدا کنی فقط کافیه اسم هنرمند و آهنگ رو سرچ کنی")
            return bot.send_message(chatid, "به این صورت: اسم خواننده - اسم آهنگ", reply_markup=startmarkup)
        if(language == "EN"):
            startmarkup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
            itembtn1 = types.KeyboardButton('📍Telegram Channel')
            itembtn2 = types.KeyboardButton('📣Advertisements')
            itembtn3 = types.KeyboardButton('☎️Support')
            startmarkup.add(itembtn1, itembtn2, itembtn3)
            bot.send_message(chatid, "Hello, I'm music bot you can search for your favorite music here with below format, it's easy just simple step.")
            return bot.send_message(chatid, "Search in this format: performer - title", reply_markup=startmarkup)
    if type == 1: 
        if(language == "FA"):
            startmarkup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
            itembtn1 = types.KeyboardButton('📍کانال تلگرام')
            itembtn2 = types.KeyboardButton('📣تبلیغات')
            itembtn3 = types.KeyboardButton('☎️پشتیبانی')
            startmarkup.add(itembtn1, itembtn2, itembtn3)
        if(language == "EN"):
            startmarkup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
            itembtn1 = types.KeyboardButton('📍Telegram Channel')
            itembtn2 = types.KeyboardButton('📣Advertisements')
            itembtn3 = types.KeyboardButton('☎️Support')
            startmarkup.add(itembtn1, itembtn2, itembtn3)

@bot.message_handler(commands=['start'])
def command_start(message):
    return goHomePage(message.chat.id, 0)

@bot.message_handler(commands=['myid'])
def command_myid(message):
    return bot.send_message(message.chat.id, "your id: " + str(message.from_user.id))

@bot.message_handler(commands=['admins'])
def command_admins(message):
    admin = IsAdmin(message.from_user.id)
    if(admin == True):
        adminids = open("admins.txt", "r")
        for x in adminids:
            b = x.split(",")
            bot.reply_to(message, "Username: @" + str(b[1]) + " ID: " + str(b[0]))
    else: bot.reply_to(message, "Privilage is low")


def IsAdmin(uid):
    adminids = open("admins.txt", "r")
    for x in adminids:
        b = x.split(",")
        if str(uid) in str(b[0]):
            return True
            
# Saving musics in file in case you can't work with MySQL, but if you use this you have to change MySQL parts according to this function
# please don't touch it if you don't know how it works:)
'''def savemusic(uid, fileid, duration, performer, title):
    songs = open("savedmusic.txt", "a")
    songs.write(str(uid) + "," +
    str(fileid) + "," +
    str(duration) + "," +
    str(performer) + "," +
    str(title) + "\n")
    songs.close()'''

def savemusic(uid, fileid, duration, performer, title):
    try:
        sql = "INSERT INTO savedmusic (`ID`, `FILEID`, `DURATION`, `PERFORMER`, `TITLE`) VALUES (%s, %s, %s, %s, %s)"
        val = (uid, fileid, duration, performer, title)
        cursor.execute(sql, val)
        mydb.commit()
        print(cursor.rowcount, "record inserted.")
    except mysql.connector.Error as err :
        mydb.rollback()
        print("Failed to insert into MySQL table {}".format(err))

def listener(messages):
    for m in messages:
        chatid = m.chat.id
        #if m.chat.type == "group" or "supergroup": you can use this method for groups and supergroups chat
        # print("User:" + str(m.from_user.first_name) + " ID:" + str(chatid) + " Text:" + str(m.text)) enabling this option will log you user chats
        if m.chat.type == "private":
            cursor.execute("SELECT * FROM `userinfo` WHERE `ID` = '" + str(m.from_user.id) + "'")
            founduser = cursor.fetchall()
            if str(founduser) == "[]": 
                sql = "INSERT INTO userinfo (`ID`, `STEP`) VALUES (" + str(m.from_user.id) + "," + str(0) + ")"
                cursor.execute(sql)
                mydb.commit()
                return print("New userstep is now recorded " + str(m.from_user.id) + " " + str(m.from_user.first_name))
            else:
                if m.text == "⬅️":
                    cursor.execute("SELECT `STEP` FROM `userinfo` WHERE `ID` = '" + str(m.from_user.id) + "'")
                    founduser = cursor.fetchall()
                    if str(founduser[0][0]) == str(1):
                        return goHomePage(chatid, 0)
                if m.text == "🏛":
                    return goHomePage(chatid, 0)
                if m.text == "📍کانال تلگرام" or m.text == "📍Telegram Channel":
                    bot.send_message(chatid, "Your channel link here/آیدی کانال تلگرام")
                    return goHomePage(chatid, 1)
                if m.text == "📣تبلیغات":
                    bot.send_message(chatid, "Advertisements here/تبلیغات")
                    return goHomePage(chatid, 1)
                if m.text == "☎️پشتیبانی" or m.text == "☎️Support":
                    if language == "FA":
                        bot.send_message(chatid, "این ربات توسط دکتر کد کدنویسی شده، ارتباط با طراح drcodee@yahoo.com")
                    if language == "EN":
                        bot.send_message(chatid, "This bot is coded by drcodee, contact us: drcodee@yahoo.com")
                    return goHomePage(chatid, 1)
                if m.content_type == "audio":
                    if IsAdmin(m.from_user.id):
                        cursor.execute("SELECT `TITLE` from `savedmusic`")
                        songcheck = cursor.fetchall()
                        for x in songcheck:
                            if str(m.audio.title) != str(x[0]):
                                continue
                            if str(m.audio.title) == str(x[0]):
                                return bot.send_message(chatid, m.audio.performer + " " + m.audio.title + " already exists in database!")
                                break
                        savemusic(m.from_user.id, m.audio.file_id, m.audio.duration, m.audio.performer, m.audio.title)
                        bot.send_message(chatid, m.audio.performer + " " + m.audio.title + " successfuly saved to database, Thanks.")
                    return
                if ", " in m.text:
                    b = m.text.split(", ")
                    cursor.execute("SELECT * FROM `savedmusic` WHERE `PERFORMER` = '" + b[0] + "' AND `TITLE` = '" + b[1] + "'")
                    searchedmusic = cursor.fetchall()
                    for x in searchedmusic:
                        bot.send_audio(chatid, str(x[1]), '@Jaybiz_Bot 🎶🔊', str(x[2]), str(x[3]), str(x[4]))
                if " - " in m.text:
                    b = m.text.split(" - ")
                    sql = "SELECT * FROM `savedmusic` WHERE `PERFORMER` LIKE " + "'%" + b[0] + "%'"
                    cursor.execute(sql, m.text)
                    searchperformer = cursor.fetchall()
                    percount = cursor.rowcount
                    sql = "SELECT * FROM `savedmusic` WHERE `TITLE` LIKE " + "'%" + b[1] + "%'"
                    cursor.execute(sql, m.text)
                    searchtitle = cursor.fetchall()
                    titcount = cursor.rowcount
                    if percount == 0 and titcount == 0: bot.send_message(chatid, "چیزی پیدا نشد") if language == "FA" else bot.send_message(chatid, "Nothing found")
                    if percount >= 1 or titcount >= 1:
                        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
                        itembtn1 = types.KeyboardButton('⬅️')
                        itembtn2 = types.KeyboardButton('🏛')
                        if searchperformer == searchtitle:
                            markup.add(itembtn1, itembtn2)
                            num = 0
                            btn = {}
                            for x in searchperformer:
                                if num >= percount: break
                                btn[num] = types.KeyboardButton(str(x[3]) + ', ' + str(x[4]))
                                markup.add(btn[num])
                                num+=1
                            cursor.execute("UPDATE `userinfo` SET `STEP` = '" + str(1) + "' WHERE `ID` = '" + str(m.from_user.id) + "'")
                            mydb.commit()
                            if language == "FA":
                                bot.send_message(chatid, "ببین برات چی پیدا کردم:", reply_markup=markup)
                            if language == "EN":
                                bot.send_message(chatid, "Here's what I found for you:", reply_markup=markup)
                        elif percount > titcount:
                            markup.add(itembtn1, itembtn2)
                            num = 0
                            btn = {}
                            for x in searchperformer:
                                if percount == 0: continue
                                num = percount
                                if num <= 0: break
                                btn[num] = types.KeyboardButton(str(x[3]) + ", " + str(x[4]))
                                markup.add(btn[num])
                                num-=1
                            cursor.execute("UPDATE `userinfo` SET `STEP` = '" + str(1) + "' WHERE `ID` = '" + str(m.from_user.id) + "'")
                            mydb.commit()
                            if language == "FA":
                                bot.send_message(chatid, "ببین برات چی پیدا کردم:", reply_markup=markup)
                            if language == "EN":
                                bot.send_message(chatid, "Here's what I found for you:", reply_markup=markup)
                        else:
                            markup.add(itembtn1, itembtn2)
                            num = 0
                            btn = {}
                            for x in searchtitle:
                                if titcount == 0: continue
                                num = titcount
                                if num <= 0: break
                                btn[num] = types.KeyboardButton(str(x[3]) + ", " + str(x[4]))
                                markup.add(btn[num])
                                num-=1
                            cursor.execute("UPDATE `userinfo` SET `STEP` = '" + str(1) + "' WHERE `ID` = '" + str(m.from_user.id) + "'")
                            mydb.commit()
                            if language == "FA":
                                bot.send_message(chatid, "ببین برات چی پیدا کردم:", reply_markup=markup)
                            if language == "EN":
                                bot.send_message(chatid, "Here's what I found for you:", reply_markup=markup)

bot.set_update_listener(listener)
bot.polling()
