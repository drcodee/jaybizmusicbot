# jaybizmusicbot - Telegram Python Bot v1.0
این ربات موزیک تلگرام به زبان پایتون توسط دکتر کد نوشته شده و باید موزیکاتون رو براش فوروارد کنین و بعدش به راحتی می تونین اونارو سرچ و استفاده کنین، یادتون نره اول ادمین های ربات رو ست کنین

This music bot is written in python language you have to forward your musics to this bot and easily search and download them, don't forget to set your bot administrators in **admins.txt** file:)

## Getting started

1. First you need to make a bot with **@BotFather** bot in telegram
2. After your bot is created you will get a token from **@BotFather**
3. Open bot.py file with any text editor or professional editors (I recommand using VSCode)
4. Search for **token = 'YOURTOKEN'** and replace your token with **YOURTOKEN**
5. Now you have to setup your MySQL database in bot
```python
DB_NAME = 'database'
mydb = mysql.connector.connect(
    host="host",
    user="username",
    passwd="password",
)
```
6. Replace **database, host, username, password** with your MySQL database information
7. Save your modifications and run the bot
8. **/start** your bot and send get your id with **/myid** command and copy your id
9. go to **admins.txt** file in your bot directory and add administrators with this format
```python
id,username
id,username
```
10. paste your copied **id** here and **username is optional** it is just to remind you who you set to admin, you can use **NoUsername** instead but don't leave it empty, **you can set how many admins you want.**
* **Example**:
```python
425562679,DrCodee
625759755,Michael
```
11. Now start forwarding your musics to the bot to get them saved in database, and it could be searched with this format:
> performer-title

## Bot Commands

Command | Usage
------------ | -------------
/start | To start the bot
/myid | Shows your telegram ID **(useful to set admins)**
/admins | Shows admins list

## Updates & Fixes
* این اولین ورژن ربات موزیک هستش و آپدیت های جدید با قابلیت های جدید براش در نظر گرفتیم برای اطلاع سریع از آپدیت ها وارد کانال تلگرام ما شوید

* This is version 1.0 of this bot, I will get this updating time to time, join our telegram channel to stay alert!

- Telegram: [Join Telegram Channel](https://t.me/DrCodee)
- Instagram: [Follow Instagram](https://www.instagram.com/DrCodee)
