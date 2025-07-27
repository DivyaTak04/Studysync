import os

class Config:
    SECRET_KEY = 'divya@004'  # Change this to a strong secret key
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:ADMIN123@localhost/studysync'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
