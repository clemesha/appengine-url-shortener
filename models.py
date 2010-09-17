import logging

from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.api import memcache


class Link(db.Model):
    user = db.UserProperty()
    url = db.LinkProperty()
    custom_path = db.BooleanProperty(default=False)
    count = db.IntegerProperty(default=0)
    created = db.DateTimeProperty(auto_now_add=True)
