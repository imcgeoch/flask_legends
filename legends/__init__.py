import os

import click

from flask import Flask
from flask_migrate import Migrate
from flask.cli import FlaskGroup, with_appcontext

from config import Config
from legends.explorer import views

from .dfparser.folder import process_directory 


def create_app(test_config=None):
    app=Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'legends.db')
            )

    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_object(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from legends.models import db
    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(explorer.views.bp)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.cli.command('import_legends')
    @click.argument('directory_path')
    def import_legends(directory_path):
        process_directory(directory_path)

    return app
