"""
Configurations for flask application. These are global variables that the app will use in its entire
lifetime
"""
import os
from abc import ABCMeta

basedir = os.path.abspath(os.path.dirname(__file__))
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    """
    Default configuration for application
    This is abstract and thus will not be used when configuring the application. 
    the instance variables and class variables will be inherited by subclass
    configurations and either they will be used as is of there will be overrides
    :cvar THREADS_PER_PAGE: Application threads. A common general assumption is
    using 2 per available processor cores - to handle
    incoming requests using one and performing background operations using the other.
    :cvar CSRF_SESSION_KEY Use a secure, unique and absolutely secret key for signing
     the data.
    :cvar SQLALCHEMY_DATABASE_URI Define the database - we are working with SQLite for
     this example    
    """

    __abstract__ = True
    __metaclass__ = ABCMeta
    SSL_DISABLE = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'reddisbot')

    # DATABASE CONFIGS
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_DB = os.environ.get("POSTGRES_DB")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    DATABASE_CONNECT_OPTIONS = {}

    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", 'reddit_salt')

    # task configurations
    REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET")
    REDDIT_APP_NAME = os.environ.get("REDDIT_APP_NAME")
    REDDIT_REDIRECT_URI = os.environ.get("REDDIT_REDIRECT_URI")
    REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID")

    # OAUTH CONFIGS from facebook
    FACEBOOK_PAGE_ACCESS_TOKEN = os.environ.get("FACEBOOK_PAGE_ACCESS_TOKEN")
    FACEBOOK_WEBHOOK_VERIFY_TOKEN = os.environ.get("FACEBOOK_WEBHOOK_VERIFY_TOKEN")

    ROOT_DIR = APP_ROOT
    WTF_CSRF_ENABLED = True
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = os.environ.get("CSRF_SESSION_KEY")
    THREADS_PER_PAGE = 2

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = True

    # gmail authentication
    MAIL_SUBJECT_PREFIX = '[Arco]'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SENDER = 'Arco Admin <arcoadmin@arco.com>'
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")

    @staticmethod
    def init_app(app):
        """Initializes the current application"""
        pass


class DevelopmentConfig(Config):
    """Configuration for development environment"""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(Config):
    """
    Testing configurations
    """

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
    """
    Production configuration
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    ADMINS = [os.environ.get("ADMIN_EMAIL_1")]

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.MAIL_SENDER,
            toaddrs=[cls.ADMINS],
            subject=cls.MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class HerokuConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config = {
    'develop': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    "heroku": HerokuConfig,
    'unix': UnixConfig,
}
