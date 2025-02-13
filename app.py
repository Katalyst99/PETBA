#!/usr/bin/env python3
""" Starts a Flask Web Application """
import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from datetime import timedelta
from db import Database, db
from routes.auth_routes import auth_bp, jwt
from routes.trans_routes import transaction_bp
from routes.budget_routes import budget_bp
from routes.summary_routes import summary_bp


def create_app(testing=False):
    """App factory function"""
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})
    if testing:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            'mysql+mysqlconnector://petba_user:Katalyst@99@localhost/test_db'
        )
    else:
        app.config.from_object(Database)

    app.config['JWT_SECRET_KEY'] = os.urandom(24)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(transaction_bp, url_prefix="/transactions")
    app.register_blueprint(budget_bp, url_prefix="/budgets")
    app.register_blueprint(summary_bp, url_prefix="/summary")

    @app.route("/", methods=["GET"])
    def serve_index():
        """Serves the index.html file."""
        return send_from_directory("frontend", "index.html")

    @app.route("/<path:filename>", methods=["GET"])
    def serve_static(filename):
        """Serve static files such as CSS and JS."""
        return send_from_directory("frontend", filename)

    @app.errorhandler(422)
    def handle_unprocessable_entity(error):
        """Error handling"""
        return jsonify(error=str(error)), 422

    return app


app = create_app()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
