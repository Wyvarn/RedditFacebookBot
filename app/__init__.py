# coding=utf-8
"""
This defines the application module that essentially creates a new flask app object
"""
import jinja2
from config import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class RedditBotApp(Flask):
    """
    Custom application class subclassing Flask application. This is to ensure more modularity in
     terms of static files and templates. This way a module will have its own templates and the
      root template folder will be more modularized and easier to manage
    """

    def __init__(self):
        """
        jinja_loader object (a FileSystemLoader pointing to the global templates folder) is being
        replaced with a ChoiceLoader object that will first search the normal FileSystemLoader and
        then check a PrefixLoader that we create
        """
        Flask.__init__(self, __name__, static_folder="static", template_folder="templates")
        self.jinja_loader = jinja2.ChoiceLoader([
            self.jinja_loader,
            jinja2.PrefixLoader({}, delimiter=".")
        ])

    def create_global_jinja_loader(self):
        """
        Overriding to return the loader set up in __init__
        :return: jinja_loader 
        """
        return self.jinja_loader

    def register_blueprint(self, blueprint, **options):
        """
        Overriding to add the blueprints names to the prefix loader's mapping
        :param blueprint: 
        :param options: 
        """
        Flask.register_blueprint(self, blueprint, **options)
        self.jinja_loader.loaders[1].mapping[blueprint.name] = blueprint.jinja_loader


def create_app(config_name):
    """
    Creates a new flask app instance with the given configuration
    :param config_name: configuration to use when creating the application 
    :return: a new WSGI Flask app
    :rtype: Flask
    """
    # app = Flask(__name__)
    app = RedditBotApp()

    db.init_app(app)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    error_handlers(app)
    register_app_blueprints(app)
    app_request_handlers(app)
    app_logger_handler(app)

    # this will reduce the load time for templates and increase the application performance
    app.jinja_env.cache = {}

    return app


def app_request_handlers(app):
    """
    This will handle all the requests sent to the application
    This will include before and after requests which could be used to update a user's status or the 
    database that is currently in use
    :param app: the current flask app
    """


def app_logger_handler(app):
    """
    Will handle error logging for the application and will store the app log files in a file that can 
    later be accessed.
    :param app: current flask application
    """


def error_handlers(app):
    """
    Error handlers function that will initialize error handling templates for the entire application
    :param app: the flask app
    """

    @app.errorhandler(404)
    def not_found(error):
        """
        This will handle errors that involve 404 messages
        :return: a template instructing user they have sent a request that does not exist on 
        the server
        """


def register_app_blueprints(app):
    """
    Registers the application blueprints
    :param app: the current flask app
    """
    from app.mod_home import home

    app.register_blueprint(home)
