from apscheduler.schedulers.blocking import BlockingScheduler
import sqlite3


sched = BlockingScheduler()

print('Oh i running!')

@sched.scheduled_job('cron', hour=12)
def scheduled_job():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('update available set flag=? , current =?', ['1', ''])
    conn.commit()
    conn.close()
sched.start()
