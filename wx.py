# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.mongoengine import MongoEngine
from wx_flask import Weixin

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB':"wx"}
app.config["SECRET_KEY"] = "kalashinikov"
app.config["WEIXIN_TOKEN"] = ""


db = MongoEngine(app)

weixin = Weixin(app)
app.add_url_rule('/', view_func=weixin.view_func)

@weixin(u'梦见')
def reply_dream(**kwargs):

    from model import *
    username = kwargs.get('sender')
    sender = kwargs.get('receiver')
    message_type = kwargs.get('type')
    content = kwargs.get('content', message_type)
    
    dream_name = content 
    if(dream_name != ''):
        result = DreamObject.objects(dream_name = dream_name)
        if(len(result) == 0):
            dream_content = u'找不到你的梦'
        else:
            dream_content = result[0].dream_content
        return weixin.reply(
            username, sender=sender, content=dream_content
        )


@weixin('*')
def reply_all(**kwargs):
    username = kwargs.get('sender')
    sender = kwargs.get('receiver')
    message_type = kwargs.get('type')
    content = kwargs.get('content', message_type)

    
    if message_type == 'event':
        print content
        print kwargs.get('event')
        if kwargs.get('event') == 'subscribe' or content == 'event':
            return weixin.reply(
                username, sender=sender, content=u"欢迎来到GUNNER闲扯平台！\n回复“梦见 XX”可以解梦！\n例如回复:\"梦见 小偷\"（\"梦见\"后面有空格）\n也可以给我留言哦！"
            )

    if content == 'news':
        return weixin.reply(
            username, type='news', sender=sender,
            articles=[
                {
                    'title': 'Weixin News',
                    'description': 'weixin description',
                    'picurl': '',
                    'url': 'http://xdream.info/',
                }
            ]
        )
    else:
        return weixin.reply(
            username, sender=sender, content=content
        )


app.debug=True

if __name__ == '__main__':
    app.run()


