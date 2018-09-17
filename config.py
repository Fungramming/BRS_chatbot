import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OAUTHLIB_INSECURE_TRANSPORT = 1
    OAUTHLIB_RELAX_TOKEN_SCOPE = 1
    AUTHORIZATION_BASE_PATH = 'cafe24api.com/api/v2/oauth/authorize'
    TOKEN_BASE_PATH = 'cafe24api.com/api/v2/oauth/token'
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    SCOPE = 'mall.write_application,mall.read_application,mall.read_product,mall.write_product,mall.read_design'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'chatbot_db.sqlite')


class ProductionConfig(Config):
    OAUTHLIB_INSECURE_TRANSPORT = 0


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}