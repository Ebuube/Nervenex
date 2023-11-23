from decouple import config
class Config:
    SECRET_KEY=config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS=config('SQLALCHEMY_TRACK_MODIFICATIONS',cast=bool)

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/db_name'
    DEBUG=True
    SQLALCHEMY_ECHO=True
    
class prodConfig(Config):
    pass

class testConfig(Config):
    pass

