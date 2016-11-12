from apscheduler.schedulers.blocking import BlockingScheduler
import sqlite3


sched = BlockingScheduler()


@sched.scheduled_job('cron', hour=5)
def scheduled_job():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('update available set flag=? , current =?', ['1', ''])
sched.start()
