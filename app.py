#!/usr/bin/env python3
""" Starts a Flask Web Application """
from flask import Flask, send_from_directory
from db import Database, db
from routes.auth_routes import auth_bp, jwt
from routes.trans_routes import transaction_bp
from routes.budget_routes import budget_bp
from routes.summary_routes import summary_bp

app = Flask(__name__)
app.config.from_object(Database)
app.config['JWT_SECRET_KEY'] = 'Union'


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


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
