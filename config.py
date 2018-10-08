import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OAUTHLIB_INSECURE_TRANSPORT = 1
    OAUTHLIB_RELAX_TOKEN_SCOPE = 1
    AUTHORIZATION_BASE_PATH = 'cafe24api.com/api/v2/oauth/authorize'
    TOKEN_BASE_PATH = 'cafe24api.com/api/v2/oauth/token'
    REQUEST_BASE_PATH = 'cafe24api.com/api/v2/admin'
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    REDIRECT_URL = os.environ.get('SERVER_URL')+'callback'
    SRC_BASE_URL = os.environ.get('SRC_BASE_URL')
    SRC_DEFUALT_FILE = os.environ.get('SRC_DEFUALT_FILE')
    SCOPE = 'mall.write_application,mall.read_application'+\
            ',mall.read_customer,mall.write_customer'+ \
            ',mall.read_design,mall.write_design'+\
            ',mall.read_order,mall.write_order'+\
            ',mall.read_product,mall.write_product'+\
            ',mall.read_store,mall.write_store'
    DEFAULT_DISPLAY_LOCATION_LIST = ["all"]
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'chatbot_db.sqlite')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'chatbot_db.sqlite')


class ProductionConfig(Config):
    OAUTHLIB_INSECURE_TRANSPORT = 0


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}