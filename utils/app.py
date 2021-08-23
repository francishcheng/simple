import requests
import argparse
import time
import hmac
import hashlib
import base64
import urllib.parse
import json
import json
import codecs
from datetime import datetime
import datetime as dt
import pathlib
from pathlib import Path
import os
import configparser
from ifyouxiao import judge_youxiao
import pymongo
from dateutil import parser
from dingtalk import DingTalk
def is_yang(record):
    detail = record.get('detail')
    judges = ''
    for item in detail:
        judges = judges + item['Judge'] 
    if '无效' in judges:
        return 'wuxiao'
    elif '阳' in judges:
        return 'yang'
    else:
        return 'yin'
class Handler:
    drug_number_api = '/UniversalDataInterface/DataSelect_drugNum'
    data_select_api = '/UniversalDataInterface/DataSelect_drug'
    access_token_api = '/UniversalDataInterface/validate'
    select_api = '/UniversalDataInterface/DataSelect_drug'
    drug_curve_api = '/UniversalDataInterface/DataSelect_drugCurve'
    SNcode = []
    access_token = ''

    def __init__(self, base_url, username, password, SNcode):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.SNcode = SNcode

    def get_access_token(self):
        form_data = {
            'username': self.username,
            'password': self.password,
        }
        json_data = json.dumps(form_data)
        response = requests.request("POST", self.base_url+self.access_token_api, data=json_data)
        if response.status_code == 200:
            json_data = json.loads(response.text) 
            if json_data['status'] == 1:
                print('get token sucessfully:', json_data['result']['access_token'])
                self.access_token = json_data['result']['access_token']
            else:
                print('invalid args, plz check out password and username')
    
        else:
            print('network error:', response.status_code)

    def get_drug_number(self, sTimeStart, sTimeEnd):
        if self.access_token == '':
            print('error: has not gotten access_token yet!')
            return
        form_data = {
                "access_token" : self.access_token,
                "sTimeStart": sTimeStart,
                "sTimeEnd" : sTimeEnd, 
                "SNcode": SNcode
            }

        json_data = json.dumps(form_data,)
        response = requests.request("POST", self.base_url+self.drug_number_api, data=json_data)
        if response.status_code == 200:
            json_data = json.loads(response.text)
            if json_data['status'] == 1:
                print('get drug number sucessfully:', json_data['result']['totalCount'])
                return json_data['result']['totalCount']
            else:
                print('invalid args in getting drug number')
        else:
            print('network error:', response.status_code)
    def get_record(self,pageNum, limitPageNum, sTimeStart, sTimeEnd):
        if self.access_token == '':
            print('error: has not gotten access_token yet!')
            return
        form_data = {
                "access_token" : self.access_token,
                "sTimeStart": sTimeStart,
                "sTimeEnd" :  sTimeEnd, 
                "pageNum": pageNum,
                "limitPageNum": limitPageNum,
                "SNcode": SNcode
                }
        json_data = json.dumps(form_data)
        response = requests.request("POST", self.base_url+self.data_select_api, data=json_data)
        # response.encoding='utf-8'
        if response.status_code == 200:
            json_data = json.loads(response.text)
            if json_data['status'] == 1:
                print('get drug records {i} sucessfully:'.format(i=str(pageNum)))
                return json_data['result']['recordArray']
            else:
                print('invalid args in getting drug records')
        else:
            print('network error:', response.status_code)
    
    def get_curve(self, record_id):
        if self.access_token == '':
            print('error: has not gotten access_token yet!')
            return
        form_data = {
            "access_token" : self.access_token,
            "RecordID": str(record_id)
        }

        json_data = json.dumps(form_data)
        response = requests.request("POST", self.base_url+self.drug_curve_api, data=json_data)
        # response.encoding='utf-8'
        if response.status_code == 200:
            json_data = json.loads(response.text)
            if json_data['status'] == 1:
                return json_data['result']['CurvePoint']
            else:
                print('invalid args in getting drug curve')
        else:
            print('network error:', response.status_code)

if __name__ == '__main__':
    username = 'Yingtianwanwu'
    password = 'yingtianwanwu0122'
    base_url = 'http://helmenyun.cn/index.php'
    post_img_url = 'http://58.87.111.39:5555/items/'
    access_token = 'df00ef487e8ef88887a4909d7cdaae7d7ca3977c45e44f51fe8e5adff77b7c3b'
    secret = 'SECfb0d1942f6fbef2f171ef7996d74d58cc8831cf02955ea524cf4c593d8eb981a'
    SNcode = ["8895b950c425abec", "df0bcbae87576add"]
    dingtalk = DingTalk(access_token, secret)

    while True:  
        now = datetime.now()
        last_day = datetime.now() 
        first_day = last_day + dt.timedelta(minutes=-6)
        first_day_strf = first_day.strftime("%Y%m%d%H%M%S")
        last_day_strf = last_day.strftime("%Y%m%d%H%M%S")
        print(first_day_strf)
        print(last_day_strf)

        
        handler = Handler(base_url, username, password, SNcode)
        handler.get_access_token()


        drug_number = handler.get_drug_number(first_day_strf, last_day_strf)
        records =  []
        previous_recordID = []
        for i in range(1,  int(drug_number)//100+2):
            records = records + handler.get_record(i, 100, first_day_strf, last_day_strf)
            time.sleep(2)
        print(len(records))
        msg = ''            
        for record in records:
            if record['RecordID'] not in previous_recordID:
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

                """
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
                """


                judge = is_yang(record) 
                values = []
                for key in record.keys():
                    if key!='points' and  key!='detail' and key!='IDNumber' and key!='PatientName' and key!='address' and key!='nation' and key!='BaseStation':
                        values.append(record[key])
                
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

                # end if judge!= "yang"
                previous_recordID.append(record['RecordID'])
        # print("msg", msg)
    
        response = dingtalk.msg(msg)
        print(response.text)
        print('sleep for 5 min')
        time.sleep(5*60)
