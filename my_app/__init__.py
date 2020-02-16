from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

db = SQLAlchemy()
bootstrap = Bootstrap()
migrate = Migrate()

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    from . import main
    app.register_blueprint(main.bp)

    db.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app)

    from my_app.main.models import Track

    @app.shell_context_processor
    def shell_context():
        return {
            'db': db,
            'Track': Track,
        }

    return app
