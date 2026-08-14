from mongoengine import Document , StringField  , EmailField

class User(Document):
    full_name=StringField(
        required=True,
        max_length=100
    )
    
    email = EmailField(
        required=True,
        unique=True
    )
    
    phone = StringField(
        required=True,
        unique=True,
        max_length=10
    )
    
    password=StringField(
        required=True
    )
    
    meta={
        "collection":"users"
    }