from flask import Flask, request
from dotenv import load_dotenv
from peewee import *
import os
import datetime

load_dotenv()
app = Flask(__name__)
mydb = MySQLDatabase(os.getenv('MYSQL_DATABASE'),
              user=os.getenv("MYSQL_USER"),
              password=os.getenv('MYSQL_PASSWORD'),
              host=os.getenv('MYSQL_HOST'),
              port=4000)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])


from app import routes
print(mydb)