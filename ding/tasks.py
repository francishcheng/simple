from huey.contrib.djhuey import db_task, db_periodic_task, lock_task, task, periodic_task, enqueue
from huey import crontab
from utils.ifyouxiao import judge_youxiao
import huey
from datetime import datetime
from utils.dingtalk import DingTalk
from ding.models import DingGroup
from utils.Handler import Handler
import requests
import argparse
import time
import hmac
import hashlib
import base64
import urllib.parse
import json
import codecs
from datetime import datetime
import datetime as dt
import pathlib
from pathlib import Path
import os
import configparser
import pymongo
from dateutil import parser
@db_periodic_task(crontab(minute='*/5'))
@lock_task("ding::tasks::every_five_mins")
def every_five_mins():
    # This is a periodic task that executes queries.
    dinggroups = DingGroup.objects.all()
    for dinggroup in dinggroups:
        send2group(dinggroup)

@db_task(retries=3, retry_delay=5)
# @lock_task("ding::tasks::send2group")
def send2group(dinggroup):

    username = 'Yingtianwanwu'
    password = 'yingtianwanwu0122'
    base_url = 'http://helmenyun.cn/index.php'
    post_img_url = 'http://58.87.111.39:5555/items/'
    access_token = dinggroup.access_token
    secret = dinggroup.secret
    SNcode = [i.strip() for i in dinggroup.SNcode.strip().split('\n')]
    dingtalk_client = DingTalk(access_token, secret)

    # dingtalk_client.msg(dinggroup.name + str(datetime.now()) + '\n' +str(SNcode))

    now = datetime.now()
    last_day = datetime.now() 
    first_day = last_day + dt.timedelta(minutes=-5)
    first_day_strf = first_day.strftime("%Y%m%d%H%M%S")
    last_day_strf = last_day.strftime("%Y%m%d%H%M%S")

    handler = Handler(base_url, username, password, SNcode)
    handler.get_access_token()
    
    drug_number = handler.get_drug_number(first_day_strf, last_day_strf)
    records = []

    for i in range(1,  int(drug_number)//100+2):
        records = records + handler.get_record(i, 100, first_day_strf, last_day_strf)
        time.sleep(2)
        
    # for record in records:
    #     print(record)
    for record in records:
        points = handler.get_curve(record['RecordID'])
        print('getting points')
        record['points'] = points
        Ce = int(record['ItemID'])
        C_ygz = int(record['CValue'])
        youxiao, reason, s, explain = judge_youxiao(record['points'], C_ygz, Ce)     
        print("原因 ", s)
        record['youxiao'] =  '有效' if youxiao==1 else '无效'
        record['reason'] =str(reason)
        record['reason_s'] = s
        record['explain'] = explain
        query = {
        'RecordID' : record['RecordID'] 
        }

        # upload image 
        data = {
            "points":record["points"], 
            "TABLE":  username,
            "RecordID": record["RecordID"]
        }
        headers = {
            'Connection': 'close',
        }
        json_data = json.dumps(data)
        
        response = requests.post(post_img_url, headers=headers, data=json_data)
        time.sleep(1)
        if response.status_code != 200:
            print("cannot upload img"+ str(record['RecordID'])) 


        msg = '' 
        msg += '\n\n\n---------------------------------------------\n\n\n'
        msg += '序列号' + ':  ' + record['SNcode']
        msg += '\n\n\n' 

        testTime = parser.parse(record['testTime'])
        msg += '测试时间' + ':  '+ testTime.strftime('%Y-%m-%d %H:%M:%S')
        msg += '\n\n\n' 
        msg += '项目名称' + ':  ' + '/'.join(i['sItemName'] for i in record['detail'])
        msg += '\n\n\n' 

        msg += '序号' + ':  ' + record['RecordID']
        msg += '\n\n\n' 

        msg += 'C值' + ':  ' + record['CValue']
        msg += '\n\n\n' 

        msg += 'T1值' + ':  ' + record.get('T1Value') if record.get('T1Value') is not None else ''
        msg += '\n\n\n' 

        msg += 'T2值' + ':  ' + record.get('T2Value') if record.get('T2Value') is not None else ''
        msg += '\n\n\n' 

        msg += 'T3值' + ':  ' + record.get('T3Value') if record.get('T3Value') is not None else ''
        msg += '\n\n\n' 

        msg += '批次名称' + ':  ' + record['BatchCode']
        msg += '\n\n\n' 

        msg += '设备投放地点' + ':  ' + record['BaseStation']
        msg += '\n\n\n' 
        
        # msg += '\n\n![screenshot](http://58.87.111.39/img/{TABLE}_{RecordID}.png)\n\n\n'.format(TABLE='test', RecordID=record['RecordID'])
        msg += '\n\n![screenshot](http://58.87.111.39/img/{TABLE}_{RecordID}.png)\n\n\n'.format(TABLE=username, RecordID=record['RecordID'])
        msg += ' \n\n '.join(["项目:" + i['sItemName']+ ' ,  ' + "判断结果:" + i['Judge']+ ' , ' +"浓度: " +  i['Concentration'] + ' ,'+ "参考范围:"  +i['range'] + '\n\n\n' for i in record['detail']])
        # msg += ' \n\n '+ record['youxiao']  + '\n\n\n'
        msg += '\n\n\n---------------------------------------------\n\n\n'
        msg += ' \n\n '+ record['reason']  + '\n\n\n'
        msg += '\n\n\n---------------------------------------------\n\n\n'
        msg += ' \n\n '+ record['reason_s']  + '\n\n\n'
        msg += '\n\n\n---------------------------------------------\n\n\n'
        msg += ' \n\n '+ record['explain']  + '\n\n\n'
        msg += '\n\n\n---------------------------------------------\n\n\n'

        dingtalk_client.msg(msg)
