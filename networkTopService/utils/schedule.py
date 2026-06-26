from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
def sche(save_func):
    scheduler.add_job(save_func, trigger="interval", minutes=10)
    scheduler.start()
