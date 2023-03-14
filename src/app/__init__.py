
import os
from flask import Flask
from dotenv import load_dotenv
from peewee import *

import datetime

load_dotenv()
app = Flask(__name__)
if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase("file:memory?mode=memory&cache=shared", uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306,
    )

from .models.timelinepost import TimelinePost

mydb.connect()
mydb.create_tables([TimelinePost])
mydb.close()
@app.before_request
def _db_connect():
    mydb.connect()

# This hook ensures that the connection is closed when we've finished
# processing the request.
@app.teardown_request
def _db_close(exc):
    if not mydb.is_closed():
        mydb.close()
        
from . import routes


