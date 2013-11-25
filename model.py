
import datetime
from wx import db

class User(db.Document):
    open_id = db.StringField(max_length=255,required=True)
    user_name = db.StringField(max_length=255)
    current_game = db.StringField(max_length=255)
    point = db.IntField(default=0)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    checked_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    check_count = db.IntField(default=0)
    nickname = db.StringField(default='')

class DreamObject(db.Document):
    dream_name = db.StringField(max_length=255, required=True)
    dream_content = db.StringField(required=True)

    meta = {
        'indexes': ['dream_name']
    }

class Duanzi(db.Document):
    page = db.IntField(required=True)
    content = db.StringField(required=True)
