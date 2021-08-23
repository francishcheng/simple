import json
import requests
from ding.models import Location
from utils.settings import location_dict
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
        new_sncode = []
        for sncode in self.SNcode:
            print(sncode)
            if not sncode.startswith(':'):
                # new_sncode +=  location_dict.get(sncode) if location_dict.get(sncode) is not None else []
                # try:

                    location_obj = Location.objects.get(location=sncode)
                    new_sncode += location_obj.get_sncode()

                    print(new_sncode)
                # except:
                    # pass
                    
        self.SNcode = new_sncode
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
                "SNcode": self.SNcode
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
                "SNcode": self.SNcode
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

