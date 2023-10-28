from telebot import types
import sqlite3
import re
import telebot
bot = telebot.TeleBot('5812226110:AAELv1h7xdEd1hylDNs9BIHtPeHmUrG0XnM')
class Bd:
    def name(message):
        with sqlite3.connect('bd1.db') as con:
            cur = con.cursor()
            name_play = cur.execute('SELECT name FROM users WHERE id_user==?;', (message.from_user.id,))
            name_play = name_play.fetchone()[0]
            return name_play

    def work(message):
        with sqlite3.connect('bd1.db') as con:
            cur = con.cursor()
            work_play = cur.execute('SELECT work FROM users WHERE id_user==?;', (message.from_user.id,))
            work_play = work_play.fetchone()[0]
            return work_play

    def balance(message):
        with sqlite3.connect('bd1.db') as con:
            cur = con.cursor()
            balance_play = cur.execute('SELECT balance FROM users WHERE id_user==?;', (message.from_user.id,))
            balance_play = balance_play.fetchone()[0]
            return balance_play

    def status(message):
        with sqlite3.connect('bd1.db') as con:
            cur = con.cursor()
            status = cur.execute('SELECT status FROM users WHERE id_user==?;', (message.from_user.id,))
            status = status.fetchone()[0]
            return status
    def business(message):
        with sqlite3.connect('bd1.db') as con:
            cur = con.cursor()
            business = cur.execute('SELECT business FROM users WHERE id_user==?;', (message.from_user.id,))
            business = business.fetchone()[0]
            return business
    def hour_business(message):
        with sqlite3.connect('bd1.db') as con:
            cur = con.cursor()
            hour_business = cur.execute('SELECT hour_business FROM users WHERE id_user==?;', (message.from_user.id,))
            hour_business = hour_business.fetchone()[0]
            return hour_business
    def month_business(message):
        with sqlite3.connect('bd1.db') as con:
            cur = con.cursor()
            month_business = cur.execute('SELECT day_business FROM users WHERE id_user==?;', (message.from_user.id,))
            month_business = month_business.fetchone()[0]
            return month_business
    def business_balance(message):
        with sqlite3.connect('bd1.db') as con:
            cur = con.cursor()
            business_balance = cur.execute('SELECT business_balance FROM users WHERE id_user==?;', (message.from_user.id,))
            business_balance = business_balance.fetchone()[0]
            return business_balance
    def work_work(message, item):
        with sqlite3.connect('bd1.db') as con:
            cur = con.cursor()
            work = cur.execute('SELECT work FROM works WHERE id_user==?;', (item,))
            work = work.fetchone()[0]
            return work

    def salary(message, item):
        with sqlite3.connect('bd1.db') as con:
            cur = con.cursor()
            salary = cur.execute('SELECT salary FROM works WHERE id_user==?;', (item,))
            salary = salary.fetchone()[0]
            return salary

    def buy(message, item):
        with sqlite3.connect('bd1.db') as con:
            cur = con.cursor()
            buy = cur.execute('SELECT buy FROM works WHERE id_user==?;', (item,))
            buy = buy.fetchone()[0]
            return buy
    def business_business(message, item):
        with sqlite3.connect('bd1.db') as con:
            cur = con.cursor()
            business = cur.execute('SELECT business FROM business WHERE id_user==?;', (item,))
            business = business.fetchone()[0]
            return business
    def salary_business(message, item):
        with sqlite3.connect('bd1.db') as con:
            cur = con.cursor()
            salary = cur.execute('SELECT salary FROM business WHERE id_user==?;', (item,))
            salary = salary.fetchone()[0]
            return salary
    def buy_business(message, item):
        with sqlite3.connect('bd1.db') as con:
            cur = con.cursor()
            buy = cur.execute('SELECT buy FROM business WHERE id_user==?;', (item,))
            buy = buy.fetchone()[0]
            return buy
def start_button():
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('работать')
    btn2 = types.KeyboardButton('команды')
    btn3 = types.KeyboardButton('бизнес')
    btn4 = types.KeyboardButton('профиль')
    btn5 = types.KeyboardButton('репорт')
    markup.row(btn1)
    markup.row(btn2, btn3)
    markup.row(btn4, btn5)
    return markup
def main_button(message):
    with sqlite3.connect('bd1.db') as con:
        cur = con.cursor()
        button = cur.execute('SELECT button FROM users WHERE id_user==?;', (message.from_user.id,))
        button = button.fetchone()[0]
        if button=='нет':
            markup = types.ReplyKeyboardMarkup()
            btn1 = types.KeyboardButton('работать')
            btn2 = types.KeyboardButton('команды')
            btn3 = types.KeyboardButton('бизнес')
            btn4 = types.KeyboardButton('профиль')
            btn5 = types.KeyboardButton('репорт')
            markup.row(btn1)
            markup.row(btn2, btn3)
            markup.row(btn4, btn5)
            return markup
        else:
            button_edit = cur.execute('SELECT button FROM users WHERE id_user==?;', (message.from_user.id,))
            button_edit = button_edit.fetchone()[0].split()
            button = [button_edit[2], button_edit[3], button_edit[4], button_edit[5], button_edit[6], button_edit[7]]
            markup = types.ReplyKeyboardMarkup()
            btn1 = types.KeyboardButton('работать')
            btn2 = types.KeyboardButton(button[0])
            btn3 = types.KeyboardButton(button[1])
            btn4 = types.KeyboardButton(button[2])
            btn5 = types.KeyboardButton(button[3])
            btn6 = types.KeyboardButton(button[4])
            btn7 = types.KeyboardButton(button[5])
            markup.row(btn1)
            markup.row(btn2, btn3, btn4)
            markup.row(btn5, btn6, btn7)
            return markup

def regular(message, item):
    pattern = rf'{item} (\d+)'
    match = re.match(pattern, message.text.lower())
    return match
def report(message):
    pattern = r'репорт (.+)'
    match = re.match(pattern, message.text.lower())
    return match
def edit_button(message):
    pattern = r'редактировать кнопки (.+)'
    match = re.match(pattern, message.text.lower())
    return match
def test(message):
    with sqlite3.connect('bd1.db') as con:
        cur = con.cursor()
        cur.execute('UPDATE users SET name=? WHERE id_user==?;', (message.text, message.from_user.id))
        names = cur.execute('SELECT name FROM users WHERE id_user==?;', (message.from_user.id,))
        namea = names.fetchone()[0]
        bot.send_message(message.chat.id, f'Приятно познакомиться, {namea}')
def working(message):
    with sqlite3.connect('bd1.db') as con:
        cur = con.cursor()
        workk = cur.execute('SELECT work FROM users WHERE id_user=?;', (message.from_user.id,))
        workkk = workk.fetchone()[0].lower()
        salary = cur.execute('SELECT salary FROM works WHERE work=?;', (workkk,))
        salary = salary.fetchone()[0]
        balik = cur.execute('SELECT balance FROM users WHERE id_user=?;', (message.from_user.id,))
        balik = balik.fetchone()[0]
        cur.execute('UPDATE users SET balance=? WHERE id_user=?;', (int(balik) + int(salary), message.from_user.id))
    bot.reply_to(message, f'Вы заработали {salary}₽💰. Ваш баланс: {int(balik) + int(salary)}₽🤑 ')
@bot.callback_query_handler(func=lambda callback: True)  # обработка функций каллбек
def callback_message(call):
    if call.data == 'takeoff_money':
        if Bd.business_balance(call)>0:
            with sqlite3.connect('bd1.db') as con:
                cur = con.cursor()
                balanc_play = cur.execute('SELECT balance FROM users WHERE id_user==?;', (call.from_user.id,))
                balanc_play = balanc_play.fetchone()[0]
                business_balanc_play = cur.execute('SELECT business_balance FROM users WHERE id_user==?;',(call.from_user.id,))
                business_balanc_play = business_balanc_play.fetchone()[0]
                cur.execute('UPDATE users SET balance=? WHERE id_user=?;',(balanc_play + business_balanc_play, call.from_user.id))
                cur.execute('UPDATE users SET business_balance=? WHERE id_user=?;', (0, call.from_user.id))

                balance_play = cur.execute('SELECT balance FROM users WHERE id_user==?;', (call.from_user.id,))
                balance_play = balance_play.fetchone()[0]
                bot.send_message(call.message.chat.id, f'Вы успешно сняли деньги с бизнеса. Ваш баланс: {balance_play}')
                business = Bd.business(call)
                bot.edit_message_text(f'''
Ваш бизнес: {business}
На счету вашего бизнеса: 0''', call.message.chat.id, call.message.message_id)
        else:
            bot.send_message(call.message.chat.id, 'У вас нет денег на счету бизнеса')
            business = Bd.business(call)
            bot.edit_message_text(f'''
Ваш бизнес: {business}
На счету вашего бизнеса: 0''', call.message.chat.id, call.message.message_id)
