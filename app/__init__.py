# Application Factory
import os
from flask import Flask

def create_app():

    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )

    from . import db
    db.init_app(app)

    return app
