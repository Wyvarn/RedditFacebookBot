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

    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", 'reddit_salt')

    # task configurations
    REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET")
    REDDIT_APP_NAME = os.environ.get("REDDIT_APP_NAME")
    REDDIT_REDIRECT_URI = os.environ.get("REDDIT_REDIRECT_URI")
    REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID")

    ROOT_DIR = APP_ROOT
    WTF_CSRF_ENABLED = True
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = os.environ.get("CSRF_SESSION_KEY")
    THREADS_PER_PAGE = 2

    @staticmethod
    def init_app(app):
        """Initializes the current application"""
        pass


class DevelopmentConfig(Config):
    """Configuration for development environment"""

    DEBUG = True


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

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


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