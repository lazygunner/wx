# coding:utf-8
import requests
import hashlib
import os
from urllib2 import quote

class XiaoI(object):
    app_key = ""
    app_secret = ""
    plateform = "custom"
    api_type = "0"
    nonce = ""
    sign = ""
    name = "GUNNER"

    def __init__(self, app):
        if hasattr(app, 'config'):
            config = app.config
        else:
            config = app

        self.app_key = config.get('XIAOI_KEY', None)
        self.app_secret = config.get('XIAOI_SECRET', None)
        #self.plateform = plateform
        #self.api_type = api_type
        
        realm = "xiaoi.com"
        method = "POST"
        uri = "/robot/ask.do"
        random_str = ''.join(map(lambda xx:(hex(ord(xx))[2:]), os.urandom(20)))      
        self.nonce = random_str
        ha1 = hashlib.sha1(self.app_key + ':' + realm + ':' + self.app_secret).hexdigest()
        ha2 = hashlib.sha1(method + ':' + uri).hexdigest()
        self.sign = hashlib.sha1(ha1 + ':' + self.nonce + ':' + ha2).hexdigest()

    def chat(self, question, user_id):
        
        api_uri = "http://nlp.xiaoi.com/robot/ask.do"

        payload = "question=" + quote(question.encode('utf-8'))\
            + "&userId=" + user_id + "&platform=" + self.plateform\
            + "&type=" + self.api_type 

        xauth = 'app_key="' + self.app_key + '",nonce="' + self.nonce + '",signature="' + self.sign + '"'

        headers = {"X-AUTH":xauth, "content-type":"application/x-www-form-urlencoded"}

        r = requests.post(api_uri, data=payload, headers=headers)
        content = r.text.replace(u'小i', self.name)
        content = r.text.replace('Xiao i', self.name)
        return content
        

