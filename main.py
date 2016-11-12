from telegram.ext import Updater, CommandHandler, Job
from random import choice
from time import sleep
import datetime
import sqlite3
from bot_id import TOKEN

TOKEN = TOKEN
updater = Updater(token=TOKEN)
job = updater.job_queue
dispatcher = updater.dispatcher

def pidoreg(bot, update):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    user_id = '@' + update.message.from_user.username
    c.execute('SELECT * from pidors')
    allpid = c.fetchall()
    getall = [x[1] for x in allpid]
    if user_id in getall:
        update.message.reply_text('Ей, ты уже в игре!')
    else:
        c.execute("INSERT INTO pidors('pidor', 'wich_group', 'score') VALUES (? ,?, ?)", [user_id, update.message.chat.username, 0])
        conn.commit()
        conn.close()
        update.message.reply_text(
            'Ты регнулся, {}'.format(user_id))


def showpid(bot, update):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('SELECT * from pidors')
    allpid = c.fetchall()
    pidout = ''
    pidlen = len(allpid)
    for x in allpid:
        pidout += '\n'
        pidout += x[1]

    if not allpid:
        update.message.reply_text('Пидоров нет. Будь первым! \n Жми /regpi')
    else:
        update.message.reply_text('Кандидаты в пидоры дня: %s \n Хочешь себя увидеть тут? \n Жми /regpi' %(pidout))


def choose_pid(bot, update):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    group_name = update.message.chat.username
    result = c.execute("select * from pidors where wich_group=?", [group_name]).fetchall()
    control_result = c.execute("select * from available WHERE group_telega=?", [group_name]).fetchall()
    if int(control_result[0][2]) != 0:
        id_for_random = [x[0] for x in result]
        winner = choice(id_for_random)
        winner_info = c.execute("select * from pidors where id=?", (winner,)).fetchall()
        heap_start_messages_first = [
            'Инициализирую поиск пидора дня...',
            'Внимание, ищу пидора!',
            'Ну-ка дай-ка...',
            'Такс, кто тут у нас мало каши ел?',
            'Инициализация.Поиск.'
        ]
        heap_start_messages_last = [
            'Кажется я что-то вижу!',
            'Не может быть!',
            'Пожалуй препроверю...',
            'Найден!'
        ]

        winner_score = int(winner_info[0][3]) + 1

        winner_data = [
            winner_score,
            winner_info[0][0],
        ]
        available_data = [
            0, group_name
        ]
        available_data_set = [
            winner_info[0][1], group_name
        ]
        c.execute('UPDATE pidors set score=? where id=?', winner_data)
        c.execute('UPDATE available set flag=? WHERE group_telega=?', available_data)
        c.execute('UPDATE available set current=? WHERE group_telega=?', available_data_set)
        conn.commit()
        conn.close()
        bot.sendMessage(chat_id=update.message.chat_id, text=choice(heap_start_messages_first))
        sleep(2)
        bot.sendMessage(chat_id=update.message.chat_id, text=choice(heap_start_messages_last))
        sleep(2)
        bot.sendMessage(chat_id=update.message.chat_id, text='Ага! 🎉🎉🎉 Сегодня пидор - ' + winner_info[0][1])
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Сегодня у нас уже есть победитель: ' + str(control_result[0][3]))


def stat(bot, update):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    group_name = update.message.chat.username
    data = [
        group_name,
    ]
    getlist = c.execute("select * from pidors where wich_group=? ORDER BY score DESC", data).fetchall()
    getlist_final = {
        'name': [],
        'score': [],
    }
    for pidor in getlist:
        if int(pidor[3]) == 0:
            continue
        else:
            getlist_final['name'].append(pidor[1])
            getlist_final['score'].append(pidor[3])


    output = {}
    output['name'] = []
    output['score'] = []
    for key in getlist_final['name']:
        output['name'].append(key)
    for value in getlist_final['score']:
        output['score'].append(value)

    render = [(name, score) for name, score in zip(getlist_final.get('name'), getlist_final.get('score'))]
    is_empty_stat = False
    output = 'Статистика:\n'
    for userdata in render:
        output += userdata[0] + ': ' + str(userdata[1]) + ' \n'

    bot.sendMessage(chat_id=update.message.chat_id, text=output)





def callback_minute(bot, job):
    pass

job_minute = Job(callback_minute, 60.0 * 60.0 * 24.0)
job.put(job_minute, next_t=0.0)


pidoreg_handler = CommandHandler('regpi', pidoreg)
showpid_handler = CommandHandler('showpid', showpid)
chooce_handler = CommandHandler('pidor', choose_pid)
stat_handler = CommandHandler('pidorstat', stat)

dispatcher.add_handler(pidoreg_handler)
dispatcher.add_handler(showpid_handler)
dispatcher.add_handler(chooce_handler)
dispatcher.add_handler(stat_handler)

updater.start_polling()
updater.idle()

