import os

from flask import Flask
from flask_migrate import Migrate

from config import Config
from legends import explorer


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

    app.register_blueprint(explorer.bp)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
