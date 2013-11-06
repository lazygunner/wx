#-*- coding:utf8 -*-

from flask import request, make_response, Blueprint
import hashlib
from wx import app
import xml.etree.ElementTree as ET


view = Blueprint('view', __name__, template_folder='templates')

@app.route('/', methods= ['GET', 'POST'])
def wechat_auth():
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
        MsgType = xml_resv.find("MsgType").text

        if(MsgType == "text"):
            Content = xml_recv.find("Content").text
            reply = "<xml><ToUserName><![CDATA[%s]]>" +\
                "</ToUserName><FromUserName><![CDATA[%s]]>" +\
                "</FromUserName><CreateTime>%s</CreateTime>" +\
                "<MsgType><![CDATA[text]]>" +\
                "</MsgType><Content><![CDATA[%s]]></Content>" +\
                "<FuncFlag>0</FuncFlag></xml>"
            response = make_response(reply % (FromUserName, ToUserName, 
            str(int(time.time())), 'HaHa:' + Content ) )
            response.content_type = 'application/xml'
            return response
