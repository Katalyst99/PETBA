#!/usr/bin/env python3
""" Starts a Flask Web Application """
from flask import Flask
from from db import Database, db
from routes.auth_routes import auth_bp
from routes.transaction_routes import transaction_bp
from routes.budget_routes import budget_bp

app = Flask(__name__)
app.config.from_object(Database)


db.init_app(app)


app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(transaction_bp, url_prefix="/transactions")
app.register_blueprint(budget_bp, url_prefix="/budgets")

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
