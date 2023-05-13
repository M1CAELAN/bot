import datetime
import calendar
import telebot
import psycopg2
from telebot import types


time = datetime.datetime.now()
c = calendar.TextCalendar(calendar.MONDAY)
string = c.formatmonth(time.year, time.month)

conn = psycopg2.connect(database="laba_6",
                        user="postgres",
                        password="password",
                        host="localhost",
                        port="5432")


def get_week_num(day, month, year):
    calendar_ = calendar.TextCalendar(calendar.MONDAY)
    if int(month) >= 9:
        start_month = 9
    else:
        start_month = 2
    days_by_week = []
    lenn = 0
    for i in range(start_month, month+1):
        lines = calendar_.formatmonth(year, i).split('\n')
        days_by_week = days_by_week + [week.lstrip().split() for week in lines[2:-1]]
        for j in range(lenn, lenn+len(lines[2:-1])):
            for k in range(len(days_by_week[j])):
                days_by_week[j][k] = days_by_week[j][k] + "." + str(i)
        lenn += len(lines[2:-1])
    for i, week in enumerate(days_by_week):
        if len(week) != 7 and i != 0 and i != len(days_by_week) - 1:
            days_by_week[i] = days_by_week[i] + days_by_week[i+1]
            days_by_week.remove(days_by_week[i+1])
    element = str(day) + "." + str(month)
    for index, week in enumerate(days_by_week):
        if element in week:
            return index + 1

token = "token"

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Понедельник", "Вторник")
    keyboard.row("Среда", "Четверг")
    keyboard.row("Пятница", "Суббота")
    keyboard.row("Расписание на текущую неделю")
    keyboard.row("Расписание на следующую неделю")
    bot.send_message(message.chat.id, 'Привет! Хочешь узнать свежую информацию о МТУСИ?', reply_markup=keyboard)
@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, '—————————\n'
                                    'Эмалированное судно\n'
                                    'Окошко, тумбочка, кровать-\n'
                                    'Жить тяжело и неуютно\n'
                                    'Зато уютно умирать\n'
                                    'Эмалированное судно\n'
                                    'Окошко, тумбочка, кровать, –\n'
                                    'Жить тяжело и неуютно\n'
                                    'Зато уютно умирать\n'
                                    'И тихо капает из крана\n'
                                    'И жизнь, растрепана, как блядь\n'
                                    'Выходит как бы из тумана\n'
                                    'И видит: тумбочка, кровать...\n'
                                    'И я пытаюсь приподняться\n'
                                    'Хочу в глаза ей поглядеть\n'
                                    'Взглянуть в глаза и – разрыдаться\n'
                                    'И никогда не умереть, никогда не умереть\n'
                                    'Никогда не умереть, никогда не умереть, никогда не умереть\n'
                                    'Эмалированное судно\n'
                                    'Окошко, тумбочка, кровать, –\n'
                                    'Жить тяжело и неуютно\n'
                                    'Зато уютно умирать\n'
                                    'Эмалированное судно\n'
                                    'Окошко, тумбочка, кровать, –\n'
                                    'Жить тяжело и неуютно\n'
                                    'Зато уютно умирать')


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "хочу":
        bot.send_message(message.chat.id, 'Тогда тебе сюда - https://mtuci.ru/')
    if message.text.lower() == "не хочу":
        bot.send_message(message.chat.id, 'Демократия - лажа, тебе сюда - https://mtuci.ru/')
    if message.text.lower() == "помощь":
        start_message(message)
    if message.text.lower() == "дата":
        a = str(datetime.date.today())
        a = a.split("-")
        bot.send_message(message.chat.id, str(get_week_num(int(a[2]), int(a[1]), int(a[0]))))
    start_message(message)
bot.polling(none_stop=True, interval=0)