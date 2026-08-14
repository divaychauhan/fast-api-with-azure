from mongoengine import connect
from config.settings import MONGODB_DB , MONGODB_URI

def connect_database():
    connect(db=MONGODB_DB,host=MONGODB_URI)