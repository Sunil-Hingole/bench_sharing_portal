# config.py
import os

class Config:
    SECRET_KEY = 'pass@123'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # or another database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
