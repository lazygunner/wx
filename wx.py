# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB':"wx"}
app.config["SECRET_KEY"] = "kalashinikov"

db = MongoEngine(app)

def register_blueprints(app):
    from views import view
    app.register_blueprint(view)
register_blueprints(app)


app.debug=True

if __name__ == '__main__':
    app.run()


