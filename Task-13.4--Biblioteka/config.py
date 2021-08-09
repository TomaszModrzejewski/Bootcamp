import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))    # 1

class Config:
   SECRET_KEY = os.environ.get("SECRET_KEY") or "remember-to-add-secret-key"    # 2
   SQLALCHEMY_DATABASE_URI = (                           # 3
           os.environ.get('DATABASE_URL') or
           'sqlite:///' + os.path.join(BASE_DIR, 'biblioteka.db')
   )
   SQLALCHEMY_TRACK_MODIFICATIONS = False

config = Config()