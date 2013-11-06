#-*- coding:utf8 -*-

from flask import request, make_response, Blueprint
import hashlib
from wx import app
import xml.etree.ElementTree as ET
import time

view = Blueprint('view', __name__, template_folder='templates')

@app.route('/', methods= ['GET', 'POST'])
def wechat_auth():
    
    text_reply = "<xml><ToUserName><![CDATA[%s]]>" +\
             "</ToUserName><FromUserName><![CDATA[%s]]>" +\
             "</FromUserName><CreateTime>%s</CreateTime>" +\
             "<MsgType><![CDATA[text]]>" +\
             "</MsgType><Content><![CDATA[%s]]></Content>" +\
             "<FuncFlag>0</FuncFlag></xml>"


    if request.method == 'GET':
        token = 'lazygunner'
        query = request.args
        signature = query.get('signature', '')
        timestamp = query.get('timestamp', '')
        nonce = query.get('nonce', '')
        echostr = query.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)
            
    if request.method == 'POST':
        xml_recv = ET.fromstring(request.data)
        ToUserName = xml_recv.find("ToUserName").text  
        FromUserName = xml_recv.find("FromUserName").text
        MsgType = xml_recv.find("MsgType").text

        if(MsgType == "text"):
            Content = xml_recv.find("Content").text
            response = make_response(text_reply % \
                (FromUserName, ToUserName, \
                str(int(time.time())), 'HaHa:' + Content ) )
            response.content_type = 'application/xml'
            return response
        
        elif(MsgType == 'event'):
            Event = xml_recv.find("Event").text
            if(Event == 'subscribe'):
                Content = xml_recv.find("Content").text
                    response = make_response(text_reply % \
                    (FromUserName, ToUserName, \
                    str(int(time.time())), 'Welcome to Gunner\'s WeiXin!') )
                response.content_type = 'application/xml'
                return response
            elif(Event == 'unsubscribe'):
                return ''

