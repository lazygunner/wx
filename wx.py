# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.mongoengine import MongoEngine
from wx_flask import Weixin
from games import GuessNum
import json

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB':"wx"}
app.config["SECRET_KEY"] = "kalashinikov"
app.config["WEIXIN_TOKEN"] = ""


db = MongoEngine(app)

weixin = Weixin(app)
app.add_url_rule('/', view_func=weixin.view_func)

@weixin(u'梦见')
def reply_dream(**kwargs):

    from model import DreamObject 
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

@weixin(u'游戏')
def reply_game(**kwargs):
    
    from model import User 
    username = kwargs.get('sender')
    sender = kwargs.get('receiver')
    message_type = kwargs.get('type')
    content = kwargs.get('content', message_type)
    
    user = User.objects(open_id = username)
    if len(user) == 0:
        user = User()
        user.open_id = username
        user.save()

    if message_type == 'text':
        return weixin.reply(
            username, sender=sender, content=u'回复\"猜数字\"开始按照GUNNER提示进行猜数字！')

@weixin(u'猜数字')
def reply_guess_num(**kwargs):
    from model import User
    username = kwargs.get('sender')
    sender = kwargs.get('receiver')
    user = User.objects.get(open_id = username)
    guess_num = GuessNum()
    content = guess_num.game_routine()
    guess_num_s = {'count':guess_num.count,'num':guess_num.num}
    user.current_game = json.dumps(guess_num_s)
    user.save()

    return weixin.reply(username, sender=sender, content=content)    

@weixin('*')
def reply_all(**kwargs):
    from model import User
    username = kwargs.get('sender')
    sender = kwargs.get('receiver')
    message_type = kwargs.get('type')
    content = kwargs.get('content', message_type)
    
    
    if message_type == 'event':
        event = kwargs.get('event')
        if event == 'subscribe':
            user = User.objects(open_id = username)
            if len(user) == 0:
                user = User()
                user.open_id = username
                user.save()
            return weixin.reply(
                username, sender=sender, content=u"欢迎来到GUNNER闲扯平台！\n回复“梦见 XX”可以解梦！\n例如回复:\"梦见 小偷\"（\"梦见\"后面有空格）\n也可以给我留言哦！"
            )
        elif event == 'unsubscribe':
            pass
    
    if message_type == 'voice':
        recognition = kwargs.get('recognition')
        return weixin.reply(
                username, sender=sender, content=recognition
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


