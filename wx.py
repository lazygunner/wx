# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.mongoengine import MongoEngine
from wx_flask import Weixin
from games import GuessNum
from xiaoi_api import XiaoI
import json
import datetime

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB':"wx"}
app.config["SECRET_KEY"] = "kalashinikov"
app.config["WEIXIN_TOKEN"] = ""
app.config["XIAOI_KEY"] = "aJin1z1o3rO4"
app.config["XIAOI_SECRET"] = "iaYtLxk3P3dDlQBTH61i"


db = MongoEngine(app)

weixin = Weixin(app)
app.add_url_rule('/', view_func=weixin.view_func)

xiaoi = XiaoI(app)


@weixin(u'名字')
def reply_name(**kwargs):
    from model import User 
    username = kwargs.get('sender')
    sender = kwargs.get('receiver')
    message_type = kwargs.get('type')
    content = kwargs.get('content', message_type)
    user = User.objects.get(open_id=username)
    user.update(set__nickname=content)

    content = u'名字设置成功:%s' %content
    return weixin.reply(
        username, sender=sender, content=content
    )   

@weixin(u'积分榜')
def reply_point(**kwargs):
    from model import User 
    username = kwargs.get('sender')
    sender = kwargs.get('receiver')
    message_type = kwargs.get('type')
    content = kwargs.get('content', message_type)
   
    users = User.objects.order_by('-point')[:10]
    i = 1
    content = ''
    for user in users:
        content = content + u'%d.%s | %d分\n' %(i, user.nickname, user.point)
        i = i + 1
    content = content + u'如果没有显示你的名字，可以通过回复【名字 XXX】来设置名字!（中间有空格哦！）'
    return weixin.reply(
        username, sender=sender, content=content
    )   

@weixin(u'积分')
def reply_check(**kwargs):
    from model import User 
    username = kwargs.get('sender')
    sender = kwargs.get('receiver')
    message_type = kwargs.get('type')
    content = kwargs.get('content', message_type)
   
    user = User.objects.get(open_id = username)
    content = u'当前积分为%d' %user.point
    return weixin.reply(
        username, sender=sender, content=content
    )   

@weixin(u'签到')
def reply_check(**kwargs):
    from model import User 
    username = kwargs.get('sender')
    sender = kwargs.get('receiver')
    message_type = kwargs.get('type')
    content = kwargs.get('content', message_type)
   
    user = User.objects(open_id = username)
    if len(user) == 0:
        user = User()
        user.open_id = username
        user.check_count = 1
        user.save()
    else:
        try:
            last_checked_day = user[0].checked_at.replace(hour=0,minute=0,second=0,microsecond=0)
            c = user[0].check_count
            delta = datetime.datetime.now() - last_checked_day
            delta_days = delta.days
            if delta_days < 1:
                content=u'今日已签过了, 已连续签到%d日' %user[0].check_count
            elif delta_days < 2 and delta_days >= 1:
                user[0].update(inc__check_count=1)
                content=u'签到完成, 已连续签到%d日' %user[0].check_count
                user[0].update(inc__point=user[0].check_count)
            else:
                user[0].update(set__check_count=1)
                content=u'签到完成, 已连续签到%d日' %user[0].check_count
                user[0].update(inc__point=user[0].check_count)

        except:
            user[0].update(set__check_count=1)
            content=u'签到完成, 已连续签到%d日' %user[0].check_count
            user[0].update(inc__point=user[0].check_count)
        
        finally:
            user[0].update(set__checked_at=datetime.datetime.now())
        
            return weixin.reply(
                username, sender=sender, content=content
            )   


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
    guess_num_s = {'name':guess_num.name,'count':guess_num.count,'num':guess_num.num, 'state':guess_num.state}
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
                username, sender=sender, content=u"欢迎来到GUNNER闲扯平台！\n回复“梦见 XX”可以解梦！\n例如回复:\"梦见 小偷\"（\"梦见\"后面有空格）\n回复\"游戏\"可以玩游戏!游戏有积分！\n回复【签到】,每天进行签到，签到有积分！\n回复【积分】查看积分\n闲的蛋疼可以聊天！\n也可以给我留言哦！"
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
        user = User.objects(open_id=username)
        if len(user) > 0 and content.isdigit():
            game_json = user[0].current_game
            game = json.loads(game_json)
            if game['name'] == 'guess_num':
                guess_num = GuessNum(game['num'], int(game['count']), game['state'])
                content = guess_num.game_routine(int(content))
                game['count'] = guess_num.count
                game['state'] = guess_num.state
                if(game['state'] == 'finished'):
                    game['name'] = ''
                    count = 15 - guess_num.count
                    if count <= 0:
                        count = 0.1
                    point = count * 10
                    user[0].update(inc__point=point)
                    content = content + u'\n本次获得%d点积分' %point

                j = json.dumps(game)
                user[0].update(set__current_game=j)
            #if game['name'] == '':
            #    content=u'请输入你要玩的游戏名！'
        else:
            content = xiaoi.chat(content, username)
        return weixin.reply(
            username, sender=sender, content=content
        )


app.debug=True

if __name__ == '__main__':
    app.run()


