#-*- coding:utf8 -*-

from flask import request, make_response, Blueprint
import hashlib
from wx import app


view = Blueprint('view', __name__, template_folder='templates')

@app.route('/', methods= ['GET', 'POST'])
def wechat_auth():
    if request.method == 'GET':
        token = 'lazygunner'
        query = request.args
        print query
        signature = query.get('signature', '')
        timestamp = query.get('timestamp', '')
        nonce = query.get('nonce', '')
        echostr = query.get('echostr', '')
        s = [timestamp, nonce, token]
        print s
        s.sort()
        print s
        s = ''.join(s)
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)
