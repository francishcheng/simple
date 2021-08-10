from huey.contrib.djhuey import db_task, db_periodic_task, lock_task, task, periodic_task
from huey import crontab
from datetime import datetime
from utils.dingtalk import DingTalk

@periodic_task(crontab(minute='*/1'))
# @lock_task("ding::tasks::every_five_mins")
def every_five_mins():
    # This is a periodic task that executes queries.
    access_token = 'df00ef487e8ef88887a4909d7cdaae7d7ca3977c45e44f51fe8e5adff77b7c3b'
    secret = 'SECfb0d1942f6fbef2f171ef7996d74d58cc8831cf02955ea524cf4c593d8eb981a'
    ding = DingTalk(access_token, secret) 
    ding.msg(str(datetime.now()))
    print("every five mins")
    return "every fime mines"
