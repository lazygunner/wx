import time
import hashlib

try:
    from lxml import etree
except ImportError:
    from xml.etree import cElementTree as ET
except ImportError:
    from xml.etree import ElementTree as ET


class Weixin(object):
    
    def __init__(self, app=None):
        self.token = None
        self._registry = {}

        if app:
            self.init_app(app)

    def init_app(self, app):
        if hasattr(app, 'config'):
            config = app.config
        else:
            config = app

        self.token = config.get('WEIXIN_TOKEN', None)
        self.sender = config.get('WEIXIN_SENDER', None)
        self.expires_in = config.get('WEIXIN_EXPIRES_IN', 0)

    def validate(self, signature, timestamp, nonce):
        return True
    
    def parse(self, content):
        """Parse xml body
        :param content: A text of xml body
        """
        dic = {}
        root = ET.fromstring(content)
        for child in root:
            dic[child.tag] = child.text
        ret = {}
        ret['id'] = dic.get('MsgId')
        ret['timestamp'] = int(dic.get('CreateTime', 0))
        ret['receiver'] = dic.get('ToUserName')
        ret['sender'] = dic.get('FromUserName')
        ret['type'] = type = dic.get('MsgType')

        if type == 'text':
            ret['content'] = dic.get('Content')
            return ret

        if type == 'image':
            ret['picurl'] = dic.get('PicUrl')
            return ret
        
        if type == 'location':
            ret['location_x'] = dic.get('Location_X')
            ret['location_y'] = dic.get('Location_Y')
            ret['scale'] = int(dic.get('Scale', 0))
            ret['label'] = dic.get('Label')
            return ret

        if type == 'link':
            ret['title'] = dic.get('Title')
            ret['description'] = dic.get('Description')
            ret['url'] = dic.get('url')
            return ret

        return ret

    def reply(self, username, type='text', sender=None, **kwargs):
        
        if not sender:
            sender = self.sender

        if not sender:
            raise RuntimeError('WEIXIN_SENDER is missing')

        if type == 'text':
            content = kwargs.get('content', '')
            return text_reply(username, sender, content)

        if type == 'music':
            values = {}
            for k in ('title', 'description', 'music_url', 'hq_music_url'):
                values[k] = kwargs.get(k)
            return music_reply(username, sender, **values)

        if type == 'news':
            items = kwargs.get('articles', [])
            return news_reply(user_name, sender, *item)

        return None

    def register(self, key, func=None):
        if func:
            self._registry[key] = func
            return

        return self.__call__(key)

    def __call__(self, key):
        # as decorator
        def wrapper(func):
            self._registry[key] = func
        return wrapper

    def view_func(self):
        from flask import request, Response

        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        if not self.validate(signature, timestamp, nonce):
            return 'signature failed', 400

        if request.method == 'GET':
            echostr = request.args.get('echostr')
            return echostr

        try:
            ret = self.parse(request.data)
        except:
            return 'invalid', 400

        if 'type' not in ret:
            return 'invalid', 400


        if ret['type'] == 'text' and ret['content'] in self._registry:
            func = self._registry[ret['registry']]
        elif '*' in self._registry:
            func = self._registry['*']
        else:
            func = 'failed'

        if callable(func):
            text = func(**ret)
        else:
            text = self.reply(
                username = ret['sender'],
                sender = ret['reciver'],
                content = func,
            )
        return Response(text, content_type='text/xml;charset=utf-8')

    view_func.methods = ['GET', 'POST']



            














