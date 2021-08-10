import json, time, hmac, hashlib, base64, codecs, urllib.parse, requests
class DingTalk():
    def __init__(self, access_token, secret):
        self.access_token = access_token
        self.secret = secret
    def get_params(self):
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return timestamp, sign
    def msg(self, markdown_text):
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "test",
                "text": markdown_text

            },
            "at": {
                "isAtAll": False
            }
        }
        json_data = json.dumps(data)
        print(json_data)
        timestamp, sign = self.get_params()
        print(timestamp, sign)
        response = requests.post(
            url='https://oapi.dingtalk.com/robot/send?access_token={access_token}&sign={sign}&timestamp={timestamp}'.format(access_token=self.access_token, sign=sign, timestamp=timestamp), data=json_data, headers=headers)
        return response


if __name__ == '__main__':
    access_token = 'df00ef487e8ef88887a4909d7cdaae7d7ca3977c45e44f51fe8e5adff77b7c3b'
    secret = 'SECfb0d1942f6fbef2f171ef7996d74d58cc8831cf02955ea524cf4c593d8eb981a'
    ding = DingTalk(access_token, secret) 
    ding.msg('test')
