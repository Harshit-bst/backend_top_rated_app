import datetime
from collections import OrderedDict
from flask import current_app

from extensions import db


class AndroidApp(db.Model):
    __tablename__ = 'android_app'
    id = db.Column(db.Integer, primary_key=True)
    pkg = db.Column(db.String(128), unique=True, index=True)
    name = db.Column(db.String(128), unique=True, index=True)
    corporation = db.Column(db.String(128), nullable=False, server_default='')
    image_url = db.Column(db.String(128), nullable=False, server_default='')
    details = db.Column(db.String(128), nullable=False, server_default='')
    category = db.Column(db.String(128), nullable=False, server_default='')
    created_on = db.Column(db.DateTime, default=datetime.datetime.now)