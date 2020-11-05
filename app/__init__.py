from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from app.common.error_handling import AppErrorBaseClass, ObjectNotFound, BadRequest
from app.db import db
from app.master_sound.api.router import master_sound_api
from .ext import ma, migrate
from config.default import SECRET_KEY


def create_app(settings_module):
    app = Flask(__name__)
    app.config.from_object(settings_module)

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)

    Api(app, catch_all_404s=True)

    app.url_map.strict_slashes = False
    
    app.register_blueprint(master_sound_api)

    CORS(app)

    register_error_handlers(app)

    app.secret_key = SECRET_KEY

    return app



def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception_error(e):
        return jsonify({'msg': str(e)}), 500

    @app.errorhandler(405)
    def handle_405_error(e):
        return jsonify({'msg': 'Method not allowed'}), 405

    @app.errorhandler(403)
    def handle_403_error(e):
        return jsonify({'msg': 'Forbidden error'}), 403

    @app.errorhandler(404)
    def handle_404_error(e):
        return jsonify({'msg': 'Not found error'}), 404

    @app.errorhandler(AppErrorBaseClass)
    def handle_app_base_error(e):
        return jsonify({'msg': str(e)}), 500

    @app.errorhandler(ObjectNotFound)
    def handle_object_not_found_error(e):
        return jsonify({'msg': str(e)}), 404

    @app.errorhandler(BadRequest)
    def hanlde_bad_request_data_format(e):
        return jsonify({'msg': str(e)}), 400

