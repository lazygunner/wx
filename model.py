

from wx import db

class User(db.Document):
    open_id = db.StringField(max_length=255,required=True)
    user_name = db.StringField(max_length=255)
    current_game = db.StringField(max_length=255)
    point = db.IntField(default=0)

class DreamObject(db.Document):
    dream_name = db.StringField(max_length=255, required=True)
    dream_content = db.StringField(required=True)

    meta = {
        'indexes': ['dream_name']
    }


