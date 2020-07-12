class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:wwa758341966@127.0.0.1:3306/mydb1'



class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    DATABASE_URI = ''

class TestingConfig(Config):
    TESTING = True