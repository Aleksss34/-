
import datetime
import random
import traceback
from function import *
import webbrowser

try:


    @bot.message_handler(commands=['start'])
    def start(message):
        with sqlite3.connect('bd1.db') as con:
            cur = con.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS users (id_user INTEGER, name varchar(50), balance INTEGER, work varchar(50), status varchar(50), business varchar(50), business_hour INTEGER, business_day INTEGER) ')
            cur.execute('CREATE TABLE IF NOT EXISTS works (id_user INTEGER, work varchar(50), salary INTEGER, buy INTEGER, photo varchar(50)) ')
            cur.execute('CREATE TABLE IF NOT EXISTS business (id_user INTEGER, business varchar(50), salary INTEGER, buy INTEGER, photo varchar(50)) ')
            con.commit()
            id_user = cur.execute('SELECT name FROM users WHERE id_user==?;', (message.from_user.id,))
            id_user = id_user.fetchall()
            if len(id_user) == 0:
                current_datetime = datetime.datetime.now()
                cur.execute('INSERT INTO users (id_user, name, balance, work, status, business, hour_business, day_business, business_balance, button) VALUES (?,?,?,?,?,?,?,?,?,?)',(message.from_user.id, message.from_user.first_name, 0, 'протирание фар', 'обычный пользователь','нет', current_datetime.hour, current_datetime.month, 0, 'нет'))
                bot.send_message(message.chat.id, f'приветствую, {message.chat.first_name}, я игровой бот🤖 с большим функционалом. Пиши /help или команды, чтобы узнать❓, что я могу и начинай строить свою карьеру🤑',reply_markup=start_button())

                con.commit()
            else:
                bot.send_message(message.chat.id, f'у тебя уже есть аккаунт в нашем боте🤖, напиши профиль, чтобы посмотреть свой аккаунт или помощь❓. чтобы узнать какие команды присутствуют в нашем боте', reply_markup=main_button(message))
    @bot.message_handler(commands=['help'])
    def help(message):
        bot.reply_to(message, f'''
{Bd.name(message)},мои команды:
основные⚙️:
сменить имя - поменять ваше имя в боте, 
включить/выключить кнопки🔁
работать - заработывать игровую валюту в нашем боте💰,
работы🚧 - посмотреть список работ🗒️🚧, на которые можно устроиться,
купить работу💸 [номер работы],
бизнес💵 - собрать часовые заработки🕐, ознакомиться и собрать деньги с бизнеса
купить бизнес 💸[номер] - приобрести новый бизнес
бизнесы💵 - посмотреть список бизнесов🗒️💵, которые можно приобрести
баланс💰 - посмотреть сколько у вас есть игровой валюты,
привет👋 - поприветствовать нашего бота,
передать [сумма перевода] [айди человека, которому нужно перевести]↪️💰 - передать другому пользователю игровую валюту
список пользователей🗒️👤 - ознакомиться с людьми которые играют в нашего бота,
профиль📝 - посмотреть свой профиль в нашем боте,
репорт [ваше сообщение администрации]🆘 - написать свое обращение к админу👨🏻‍💼
редактировать кнопки✍️ [кнопка 1], [кнопка 2], [кнопка 3], [кнопка 4], [кнопка 5], [кнопка 6] - редактировать кнопки под клавиатурой под себя✍️, кроме кнопки работать.

игровые🎯:
казино [сумма]🎰/ казино все - испытать удачу,
кости [число 1-12]🎲 - угадать загаданное ботом число и получить вознаграждение💵,
бот умничка👍 - похвалить бота,
бот молодец 👍 - похвалить бота''')


    @bot.message_handler(commands=['site', 'website'])
    def site(message):
         webbrowser.open('https://vk.com/id534138304')
    @bot.message_handler()
    def commands(message):
        if message.text.lower() == 'список пользователей':
            with sqlite3.connect('bd1.db') as con:
                cur = con.cursor()
                cur.execute('SELECT * FROM users')
                users = cur.fetchall()
                info = ''
                for i in users:
                    info += f'Айди: {i[0]}, Имя: {i[1]}, Баланс: {i[2]}, Работа: {i[3]} \n'
                bot.send_message(message.chat.id, info)
        elif message.text.lower() == 'сменить имя' or message.text.lower() == 'сменить ник' or message.text.lower() == 'поменять имя' or message.text.lower() == 'поменять ник':
            mesg = bot.send_message(message.chat.id, 'Напишите имя, которое вы бы хотели')
            bot.register_next_step_handler(mesg, test)
        elif message.text.lower() == 'работать':
            working(message)
        elif message.text.lower() == 'бизнес':
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('снять деньги', callback_data='takeoff_money'))

            with sqlite3.connect('bd1.db') as con:
                cur = con.cursor()
                hour = Bd.hour_business(message)
                month = Bd.month_business(message)
                current_datetime = datetime.datetime.now()
                current_month = current_datetime.month
                current_hour = current_datetime.hour
                current_day = current_datetime.day
                hour_now = int(current_hour) + int(current_day) * 24
                business = Bd.business(message)
                if business == 'нет':
                    bot.reply_to(message, ' у вас нет бизнеса😕')
                else:
                    if int(current_month)!=int(month):
                        bot.reply_to(message, 'Начался новый месяц и все что было заработано во время вашего отсутствия сгорело😕')
                        cur.execute('UPDATE users SET day_business=? WHERE id_user==?;',(current_month, message.from_user.id))


                        cur.execute('UPDATE users SET hour_business=? WHERE id_user==?;',(hour_now, message.from_user.id))
                        business = Bd.business(message)
                        busines_balance = Bd.business_balance(message)

                        bot.send_message(message.chat.id, f'''
Ваш бизнес: {business}
На счету вашего бизнеса: {busines_balance}💰''',reply_markup=markup)
                    else:

                        hour_now = int(current_hour)+int(current_day)*24
                        time = hour_now - hour
                        if time>0:

                            business_balance = Bd.business_balance(message)
                            business = Bd.business(message)
                            salary = cur.execute('SELECT salary FROM business WHERE business=?;', (business,))
                            salary = salary.fetchone()[0]
                            cur.execute('UPDATE users SET business_balance=? WHERE id_user==?;',(business_balance + time*salary, message.from_user.id))
                            cur.execute('UPDATE users SET hour_business=? WHERE id_user==?;',(hour_now, message.from_user.id))
                            bot.reply_to(message, f'Вас не было {time} часов⏰. Ваш бизнес принес за это время {time*salary}💰')
                            busines_balance = cur.execute('SELECT business_balance FROM users WHERE id_user==?;',(message.from_user.id,))
                            busines_balance = busines_balance.fetchone()[0]
                            bot.send_message(message.chat.id,f'''
Ваш бизнес: {business}
На счету вашего бизнеса: {busines_balance}💰''',reply_markup=markup)
                        else:
                            business = Bd.business(message)
                            busines_balance = Bd.business_balance(message)
                            bot.reply_to(message, 'Новый час еще не наступил, вы ничего не заработали ')
                            bot.send_message(message.chat.id, f'''
Ваш бизнес: {business}
На счету вашего бизнеса: {busines_balance}💰''',reply_markup=markup)
        elif message.text.lower() == 'профиль':
            with sqlite3.connect('bd1.db') as con:
                cur = con.cursor()
                cur.execute('SELECT * FROM users WHERE id_user==?;', (message.from_user.id,))
                users = cur.fetchall()
                info = ''
                for i in users:
                    info += f'''
Имя: {i[1]}
Статус: {i[4]}
Ваше Айди: {i[0]}
Баланс: {i[2]}
Работа: {i[3]} , Бизнес: {i[5]}


'''
                bot.send_message(message.chat.id, info)
        elif message.text.lower() == 'привет':
            bot.send_message(message.chat.id, f'приветствую🖐, {Bd.name(message)}')
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAALnGmTvxi7lfBt5ICj7jvr-LVf29u8JAAL_AgACbbBCAwSgOas0AjY3MAQ')
        elif message.text.lower() == 'бот молодец':
            bot.send_message(message.chat.id, f'спасибо🥰, всегда рад развлечь вас')
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAALnHGTvxyLBlJBd5pGYtAtQmAFr7FvAAALCEAACk0O5SCXmlKJ-lvQoMAQ')
        elif message.text.lower() == 'бот умничка':
            bot.send_message(message.chat.id, f'спасибо, {Bd.name(message)}, мне очень приятно🥰')
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAALnHmTvx0uUMa8RQPjShMRXwHE6Md4lAAKtEAACIZy5SLlfbtOO8CiqMAQ')
        elif regular(message, 'начислить'):
            if Bd.status(message)=='владелец' or Bd.status(message)=='администратор':
                if message.text.split()[1].count('к') > 0:
                    summ = message.text.split()[1].replace('к', '') + '000' * message.text.split()[1].count('к')
                else:
                    summ = message.text.split()[1]
                with sqlite3.connect('bd1.db') as con:
                    cur = con.cursor()
                    cur.execute('UPDATE users SET balance=? WHERE id_user==?;',(int(summ)+Bd.balance(message), message.from_user.id))
                    balance_play = cur.execute('SELECT balance FROM users WHERE id_user==?;', (message.from_user.id,))
                    balance_play = balance_play.fetchone()[0]
                    bot.reply_to(message, f'Вам выдано {summ}🤑, Ваш баланс:{balance_play}💰')
            else:
                bot.reply_to(message, 'Недостаточно прав для выдачи денег')
        elif message.text.lower() == 'команды' or message.text.lower() == 'помощь':
            bot.reply_to(message, f'''
{Bd.name(message)}, мои команды:
основные⚙️:
сменить имя - поменять ваше имя в боте, 
включить/выключить кнопки🔁
работать - заработывать игровую валюту в нашем боте💰,
работы🚧 - посмотреть список работ🗒️🚧, на которые можно устроиться,
купить работу💸 [номер работы],
бизнес💵 - собрать часовые заработки🕐, ознакомиться и собрать деньги с бизнеса
купить бизнес 💸[номер] - приобрести новый бизнес
бизнесы💵 - посмотреть список бизнесов🗒️💵, которые можно приобрести
баланс💰 - посмотреть сколько у вас есть игровой валюты,
привет👋 - поприветствовать нашего бота,
передать [сумма перевода] [айди человека, которому нужно перевести]↪️💰 - передать другому пользователю игровую валюту
список пользователей🗒️👤 - ознакомиться с людьми которые играют в нашего бота,
профиль📝 - посмотреть свой профиль в нашем боте,
репорт [ваше сообщение администрации]🆘 - написать свое обращение к админу👨🏻‍💼
редактировать кнопки✍️ [кнопка 1], [кнопка 2], [кнопка 3], [кнопка 4], [кнопка 5], [кнопка 6] - редактировать кнопки под клавиатурой под себя✍️, кроме кнопки работать.

игровые🎯:
казино [сумма]🎰/ казино все - испытать удачу,
кости [число 1-12]🎲 - угадать загаданное ботом число и получить вознаграждение💵,
бот умничка👍 - похвалить бота,
бот молодец 👍 - похвалить бота''')
        elif message.text.lower()=='работы':
            bot.reply_to(message,
f'''{Bd.name(message)},  1.протирание фар🧽 - заработок: 500💰, стоимость: бесплатно💰
2.дворник🧹 - заработок:2000💰, стоимость: 50000💰
3.продавец в пятерочке🧑🏻‍🌾 - заработок: 10000💰, стоимость: 500000💰
4.инженер👷🏻‍♂️ - заработок: 25000💰, стоимость: 5000000💰
5.шеф-повар👨🏻‍🍳 - заработок: 75000💰, стоимость: 25000000💰
6.программист🧑🏻‍💻 - заработок: 250000💰, стоимость: 180000000💰
7.директор крупного магазина👩🏻‍💼 - заработок: 1750000💰, стоимость: 4000000000💰
8.ученый👨🏻‍🔬 - заработок: 5000000💰, стоимость: 15000000000💰
9.летчик👨🏻✈️ - заработок: 15000000💰, стоимость: 75000000000💰
10.сотрудник aleks bot 🤖 - заработок💰: 50000000, стоимость: 450000000000💰
Пишите боту "работать" и получайте доход🤑, чтобы купить новую работу пишите боту "купить работу[номер работы]"''')
        elif message.text.lower()=='бизнесы':
            bot.reply_to(message,
f'''{Bd.name(message)},бизнесы💵:
1.автомат с кофе☕️: заработок в час:40000 💰, стоимость: 1500000💰
2.ларек с мороженым🍧: заработок в час: 100000💰, стоимость:  15000000💰
3.парикмахерская💇🏼‍♀️: заработок в час: 225000💰, стоимость:  100000000💰
4.бордель 👯‍♀️ : заработок в час:1500000💰, стоимость:  350000000💰
5.пятизвездочный отель🏨 : заработок в час: 6000000💰, стоимость:  1000000000💰
6.крупнейшие поставки оружия📦🔫: заработок в час:15000000💰, стоимость:  7.40000000000💰
7.NASA🌕: заработок в час:45000000💰, стоимость:  200000000000💰
Для того, чтобы приобрести бизнес, напишите боту "купить бизнес [номер бизнеса]"




''')





        elif message.text.lower()=='казино все' or message.text.lower()=='азино все' or message.text.lower()=='казино всё':
            if Bd.balance(message)>0:
                rand = random.randint(1, 101)

                if rand<35:
                    with sqlite3.connect('bd1.db') as con:
                        cur = con.cursor()
                        cur.execute('UPDATE users SET balance=? WHERE id_user==?;', (Bd.balance(message)+Bd.balance(message), message.from_user.id))
                        balance_play = cur.execute('SELECT balance FROM users WHERE id_user==?;', (message.from_user.id,))
                        balance_play = balance_play.fetchone()[0]
                        bot.reply_to(message, f'{Bd.name(message)}, Вы выиграли (2x)🙂.Ваш баланс: {balance_play}🤑')
                elif rand==35:
                    with sqlite3.connect('bd1.db') as con:
                        cur = con.cursor()
                        cur.execute('UPDATE users SET balance=? WHERE id_user==?;', (Bd.balance(message)+Bd.balance(message)*4, message.from_user.id))
                        balance_play = cur.execute('SELECT balance FROM users WHERE id_user==?;', (message.from_user.id,))
                        balance_play = balance_play.fetchone()[0]
                        bot.reply_to(message, f'{Bd.name(message)}, Вы выиграли (5x)🫣🙃. Ваш баланс: {balance_play}🤑')
                elif 35<rand<46:
                    bot.reply_to(message, f'{Bd.name(message)}, Баланс остается тем же😐. Ваш баланс: {Bd.balance(message)}🤨')
                elif 45<rand<76:
                    with sqlite3.connect('bd1.db') as con:
                        cur = con.cursor()
                        cur.execute('UPDATE users SET balance=? WHERE id_user==?;',(int(Bd.balance(message)-Bd.balance(message) * 0.5), message.from_user.id))
                        balance_play = cur.execute('SELECT balance FROM users WHERE id_user==?;', (message.from_user.id,))
                        balance_play = balance_play.fetchone()[0]
                        bot.reply_to(message, f'{Bd.name(message)}, Вы проиграли (0.5x)🙁. Ваш баланс: {balance_play}💰')
                elif 75<rand<86:
                    with sqlite3.connect('bd1.db') as con:
                        cur = con.cursor()
                        cur.execute('UPDATE users SET balance=? WHERE id_user==?;',(int(Bd.balance(message)- Bd.balance(message) * 0.75), message.from_user.id))
                        balance_play = cur.execute('SELECT balance FROM users WHERE id_user==?;', (message.from_user.id,))
                        balance_play = balance_play.fetchone()[0]
                        bot.reply_to(message, f'{Bd.name(message)}, Вы проиграли (0.75x)😒. Ваш баланс: {balance_play}💰')
                elif 85<rand<96:
                    with sqlite3.connect('bd1.db') as con:
                        cur = con.cursor()
                        cur.execute('UPDATE users SET balance=? WHERE id_user==?;',(int(Bd.balance(message) - Bd.balance(message) * 0.25), message.from_user.id))
                        balance_play = cur.execute('SELECT balance FROM users WHERE id_user==?;', (message.from_user.id,))
                        balance_play = balance_play.fetchone()[0]
                        bot.reply_to(message, f'{Bd.name(message)}, Вы проиграли (0.25x😣). Ваш баланс: {balance_play}💰')
                elif 95<rand<101:
                    with sqlite3.connect('bd1.db') as con:
                        cur = con.cursor()
                        cur.execute('UPDATE users SET balance=? WHERE id_user==?;',(0, message.from_user.id))
                        balance_play = cur.execute('SELECT balance FROM users WHERE id_user==?;', (message.from_user.id,))
                        balance_play = balance_play.fetchone()[0]
                        bot.reply_to(message, f'{Bd.name(message)}, Вы проиграли (0x)❌😖. Ваш баланс: {balance_play}🥲')
            else:
                bot.reply_to(message, f'{Bd.name(message)}, На балансе недостаточно средств😕. Ваш баланс: {Bd.balance(message)}💰')
        elif message.text.lower() == 'включить кнопки':
            if message.chat.type == 'private' or message.chat.type == 'group' and bot.get_chat_member(message.chat.id,message.from_user.id).status in ["administrator", "creator"]:
                bot.send_message(message.chat.id,f'{Bd.name(message)},кнопки успешно включены🙂',reply_markup=main_button(message))
            else:
                bot.send_message('Недостаточно прав❌😐. Чтобы включать кнопки в беседе нужно быть администратором или создателем')
        elif message.text.lower() == 'выключить кнопки':
            if message.chat.type == 'private' or message.chat.type == 'group' and bot.get_chat_member(message.chat.id,message.from_user.id).status in ["administrator", "creator"]:
                a = telebot.types.ReplyKeyboardRemove()
                bot.send_message(message.chat.id, f'{Bd.name(message)}, кнопки успешно выключены🙂', reply_markup=a)
            else:
                bot.send_message('Недостаточно прав❌😐. Чтобы выключать кнопки в беседе нужно быть администратором или создателем')
        elif message.text.lower() == 'баланс':
            bot.send_message(message.chat.id, f'{Bd.name(message)}, Ваш баланс: {Bd.balance(message)}₽🤑')
        if report(message):
            bot.reply_to(message, 'Ваш репорт отправлен администрации🫣')
            with sqlite3.connect('bd1.db') as con:
                cur = con.cursor()
                id_adm = cur.execute('SELECT id_user FROM users WHERE status==?;', ('владелец',))
                id_adm = id_adm.fetchone()[0]
                bot.send_message(id_adm, f'репорт от пользователя {Bd.name(message)}: {message.text[7:]}')

        if edit_button(message):
            if message.chat.type == 'private' or message.chat.type == 'group' and bot.get_chat_member(message.chat.id, message.from_user.id).status in ["administrator", "creator"]:
                button_editt = message.text.replace(',', '')
                button_edit = button_editt.split()
                if len(button_edit)==8:
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
                    bot.reply_to(message, 'кнопки успешно изменены🙃', reply_markup=markup)
                    if message.chat.type == 'private':
                        with sqlite3.connect('bd1.db') as con:
                            cur = con.cursor()
                            cur.execute('UPDATE users SET button=? WHERE id_user==?;',(button_editt, message.from_user.id))
                elif len(button_edit)<8:
                    bot.reply_to(message, f'Вы написали недостаточно кнопок({len(button_edit)-2})😕, кнопок должно быть 6 штук')
                else:
                    bot.reply_to(message, f'Вы написали слишком много кнопок({len(button_edit)-2})😕, кнопок должно быть 6 штук')
            else:
                bot.reply_to(message, 'Вы не являетесь администротором или создателем беседы❌😕. Только они могут редактировать кнопки здесь')
        if regular(message, 'купить работу'):
            number = int(message.text.split()[2])
            if 0 <= number <= 10:
                if Bd.balance(message)>=Bd.buy(message, number) and Bd.work_work(message, message.text.split()[2])!=Bd.work(message):
                    with sqlite3.connect('bd1.db') as con:
                        cur = con.cursor()
                        cur.execute('UPDATE users SET work=? WHERE id_user==?;', (Bd.work_work(message, message.text.split()[2]), message.from_user.id))
                        cur.execute('UPDATE users SET balance=? WHERE id_user==?;',(Bd.balance(message)-Bd.buy(message, message.text.split()[2]), message.from_user.id))
                        bot.reply_to(message, f'{Bd.name(message)}, Вы успешно приобрели работу {message.text.split()[2]}😏. Ваша новая работа: {Bd.work_work(message, message.text.split()[2])}😊')
                elif Bd.work_work(message, message.text.split()[2])==Bd.work(message):
                    bot.reply_to(message, f'{Bd.name(message)}, У вас уже есть данная работа😐')
                else:
                    bot.reply_to(message, f'{Bd.name(message)}, Недостаточно средств для покупки данной работы😕. Ваш баланс {Bd.balance(message)}💰')
            else:
                bot.reply_to(message, f'{Bd.name(message)}, Такой работы не существует😒')
        if regular(message, 'купить бизнес'):
            number = int(message.text.split()[2])
            if 0 <= number <= 10:
                if Bd.balance(message) >= Bd.buy_business(message, number) and Bd.business_business(message, message.text.split()[2]) != Bd.business(message):
                    with sqlite3.connect('bd1.db') as con:
                        cur = con.cursor()
                        cur.execute('UPDATE users SET business=? WHERE id_user==?;',(Bd.business_business(message, message.text.split()[2]), message.from_user.id))
                        cur.execute('UPDATE users SET balance=? WHERE id_user==?;', (Bd.balance(message) - Bd.buy_business(message, message.text.split()[2]), message.from_user.id))
                        current_datetime = datetime.datetime.now()
                        hour = Bd.hour_business(message)
                        current_hour = current_datetime.hour
                        current_day = current_datetime.day
                        hour_now = int(current_hour) + int(current_day) * 24
                        time = hour_now - hour
                        if time > 0 and Bd.business(message)!='нет':
                            business_balance = Bd.business_balance(message)
                            business = Bd.business(message)
                            salary = cur.execute('SELECT salary FROM business WHERE business=?;', (business,))
                            salary = salary.fetchone()[0]
                            cur.execute('UPDATE users SET business_balance=? WHERE id_user==?;',
                                        (business_balance + time * salary, message.from_user.id))
                            cur.execute('UPDATE users SET hour_business=? WHERE id_user==?;',
                                        (hour_now, message.from_user.id))


                            bot.reply_to(message,f'{Bd.name(message)}, Вы успешно приобрели бизнес {message.text.split()[2]}. Деньги с прошлого бизнеса собраны ({time * salary})💰. Ваш новый бизнес: {Bd.business_business(message, message.text.split()[2])}😊')
                        else:
                            bot.reply_to(message,
                                         f'{Bd.name(message)}, Вы успешно приобрели бизнес {message.text.split()[2]}😏. Ваш новый бизнес: {Bd.business_business(message, message.text.split()[2])}😊')

                elif Bd.business_business(message, message.text.split()[2]) == Bd.business(message):
                    bot.reply_to(message, f'{Bd.name(message)}, У вас уже есть данный бизнес😐')
                else:
                    bot.reply_to(message,f'{Bd.name(message)}, Недостаточно средств для покупки данной работы😕. Ваш баланс: {Bd.balance(message)}💰')
            else:
                bot.reply_to(message, f'{Bd.name(message)}, Такого бизнеса не существует😒')
        if regular(message, 'кости'):
            rand = random.randint(1, 12)
            if int(rand) == int(message.text.split()[1]) and int(message.text.split()[1])<=12:
                with sqlite3.connect('bd1.db') as con:
                    cur = con.cursor()
                    cur.execute('UPDATE users SET balance=? WHERE id_user==?;',(Bd.balance(message) + int(Bd.balance(message) * 0.1), message.from_user.id))
                    balance_play = cur.execute('SELECT balance FROM users WHERE id_user==?;', (message.from_user.id,))
                    balance_play = balance_play.fetchone()[0]
                bot.reply_to(message, f'{Bd.name(message)}, Вы угадали число🥳🎉. Вам начислено {int(Bd.balance(message) * 0.1)}💵. Ваш баланс:{balance_play}')
            elif int(message.text.split()[1])>12:
                bot.reply_to(message, f'{Bd.name(message)}, Число должно быть от 1 до 12😌')
            else:
                bot.reply_to(message, f'{Bd.name(message)}, Вы не угадали число🙁. Загаданное число {rand}. Попробуйте снова ')
        if regular(message, 'сейф'):
            rand = random.randint(1, 1000)
            if int(rand) == int(message.text.split()[1]) and int(message.text.split()[1])<=1000:
                with sqlite3.connect('bd1.db') as con:
                    cur = con.cursor()
                    cur.execute('UPDATE users SET balance=? WHERE id_user==?;',(Bd.balance(message) + int(Bd.balance(message) * 5), message.from_user.id))
                    balance_play = cur.execute('SELECT balance FROM users WHERE id_user==?;', (message.from_user.id,))
                    balance_play = balance_play.fetchone()[0]
                bot.reply_to(message, f'{Bd.name(message)}, Вы угадали число🎊🥳. Вам начислено {int(Bd.balance(message) * 5)}🤑. Ваш баланс:{balance_play}💰')
            elif int(message.text.split()[1])>1000:
                bot.reply_to(message, f'{Bd.name(message)}, Число должно быть от 1 до 1000🤨')
            else:
                bot.reply_to(message, f'{Bd.name(message)}, Вы не угадали число😕. Загаданное число {rand}. Попробуйте снова↪️ ')
        if regular(message, 'казино'):
            if message.text.split()[1].count('к') > 0:
                summ = message.text.split()[1].replace('к', '') + '000'*message.text.split()[1].count('к')
            else:
                summ = message.text.split()[1]
            if Bd.balance(message)>=int(summ) and int(summ)>0:
                rand = random.randint(1, 101)
                if rand<35:
                    with sqlite3.connect('bd1.db') as con:
                        cur = con.cursor()
                        cur.execute('UPDATE users SET balance=? WHERE id_user==?;', (Bd.balance(message)+int(summ), message.from_user.id))
                        balance_play = cur.execute('SELECT balance FROM users WHERE id_user==?;', (message.from_user.id,))
                        balance_play = balance_play.fetchone()[0]
                        bot.reply_to(message, f'{Bd.name(message)}, Вы выиграли (2x)🙂.Ваш баланс: {balance_play}🤑')
                elif rand==35:
                    with sqlite3.connect('bd1.db') as con:
                        cur = con.cursor()
                        cur.execute('UPDATE users SET balance=? WHERE id_user==?;', (Bd.balance(message)+int(summ)*4, message.from_user.id))
                        balance_play = cur.execute('SELECT balance FROM users WHERE id_user==?;', (message.from_user.id,))
                        balance_play = balance_play.fetchone()[0]
                        bot.reply_to(message, f'{Bd.name(message)}, Вы выиграли (5x)🫣🙃. Ваш баланс: {balance_play}🤑')
                elif 35<rand<46:
                    bot.reply_to(message, f'{Bd.name(message)}, Баланс остается тем же😐. Ваш баланс: {Bd.balance(message)}🤨')
                elif 45<rand<76:
                    with sqlite3.connect('bd1.db') as con:
                        cur = con.cursor()
                        cur.execute('UPDATE users SET balance=? WHERE id_user==?;',(int(Bd.balance(message)-int(summ) * 0.5), message.from_user.id))
                        balance_play = cur.execute('SELECT balance FROM users WHERE id_user==?;', (message.from_user.id,))
                        balance_play = balance_play.fetchone()[0]
                        bot.reply_to(message, f'{Bd.name(message)}, Вы проиграли (0.5x)🙁. Ваш баланс: {balance_play}💰')
                elif 75<rand<86:
                    with sqlite3.connect('bd1.db') as con:
                        cur = con.cursor()
                        cur.execute('UPDATE users SET balance=? WHERE id_user==?;',(int(Bd.balance(message)- int(summ) * 0.75), message.from_user.id))
                        balance_play = cur.execute('SELECT balance FROM users WHERE id_user==?;', (message.from_user.id,))
                        balance_play = balance_play.fetchone()[0]
                        bot.reply_to(message, f'{Bd.name(message)}, Вы проиграли (0.75x)😒. Ваш баланс: {balance_play}💰')
                elif 85<rand<96:
                    with sqlite3.connect('bd1.db') as con:
                        cur = con.cursor()
                        cur.execute('UPDATE users SET balance=? WHERE id_user==?;',(int(Bd.balance(message) - int(summ) * 0.25), message.from_user.id))
                        balance_play = cur.execute('SELECT balance FROM users WHERE id_user==?;', (message.from_user.id,))
                        balance_play = balance_play.fetchone()[0]
                        bot.reply_to(message, f'{Bd.name(message)}, Вы проиграли (0.25x😣). Ваш баланс: {balance_play}💰')
                elif 95<rand<101:
                    with sqlite3.connect('bd1.db') as con:
                        cur = con.cursor()
                        cur.execute('UPDATE users SET balance=? WHERE id_user==?;',(int(Bd.balance(message) - int(summ)), message.from_user.id))
                        balance_play = cur.execute('SELECT balance FROM users WHERE id_user==?;', (message.from_user.id,))
                        balance_play = balance_play.fetchone()[0]
                        bot.reply_to(message, f'{Bd.name(message)}, Вы проиграли (0x)❌😖. Ваш баланс: {balance_play}🥲')
            else:
                bot.reply_to(message, f'{Bd.name(message)}, На балансе недостаточно средств✖️. Ваш баланс: {Bd.balance(message)}💰')
        if regular(message, 'передать (\d+)'):
            if Bd.balance(message)>=int(message.text.split()[1]) :
                with sqlite3.connect('bd1.db') as con:
                    cur = con.cursor()
                    cur.execute('SELECT id_user FROM users WHERE id_user=?;', (int(message.text.split()[2]),))
                    result = cur.fetchone()
                    if result is None:
                        bot.reply_to(message, f'{Bd.name(message)}, Пользователь с таким id не зарегестрирован в нашем боте😣')
                    else:
                        balance_play = cur.execute('SELECT balance FROM users WHERE id_user==?;', (int(message.text.split()[2]),))
                        balance_play = balance_play.fetchone()[0]

                        cur.execute('UPDATE users SET balance=? WHERE id_user==?;',(int(Bd.balance(message) - int(message.text.split()[1])), message.from_user.id))

                        cur.execute('UPDATE users SET balance=? WHERE id_user==?;',(balance_play + int(message.text.split()[1]), int(message.text.split()[2])))
                        name_play = cur.execute('SELECT name FROM users WHERE id_user==?;',(int(message.text.split()[2]),))
                        name_play = name_play.fetchone()[0]
                        balance_play = cur.execute('SELECT balance FROM users WHERE id_user==?;', (message.from_user.id,))
                        balance_play = balance_play.fetchone()[0]
                        bot.reply_to(message, f'{Bd.name(message)}, Вы успешно передали игроку {name_play} {int(message.text.split()[1])}💰. Ваш баланс:{balance_play}🤑')
                        chat_id = int(message.text.split()[2])
                        name = cur.execute('SELECT name FROM users WHERE id_user==?;', (message.from_user.id,))
                        name = name.fetchone()[0]
                        balance = cur.execute('SELECT balance FROM users WHERE id_user==?;', (int(message.text.split()[2]),))
                        balance = balance.fetchone()[0]
                        bot.send_message(chat_id, f'{Bd.name(message)}, Вам поступил перевод💰 от игрока {name}  в размере {message.text.split()[1]}💰. Ваш баланс: {balance}🤑')
            elif Bd.balance(message)<int(message.text.split()[1]):
                bot.reply_to(message, f'{Bd.name(message)}, Недостаточно средств для передачи денег😕')



    bot.polling(none_stop=True)
except:
    print(traceback.format_exc())
    bot.polling(none_stop=True)