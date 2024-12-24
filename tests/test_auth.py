#!/usr/bin/env python3
"""The module for Authentication unittests"""
import unittest
from app import app, db
from flask_jwt_extended import create_access_token
from models.user import User


class TestAuthRoutes(unittest.TestCase):
    """Unittesting for Authentication"""
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_register(self):
        """Testing user registration"""
        response = self.app.post('/auth/register', json={
            "email": "petba@example.com",
            "password": "password@12"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("User registered successfully",
                      response.get_json()["message"])

    def testValidLogin(self):
        """Testing for valid user login"""
        with app.app_context():
            user = User(email="petba@example.com", password="password@12")
            db.session.add(user)
            db.session.commit()

        response = self.app.post('/auth/login', json={
            "email": "petba@example.com",
            "password": "password@12"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.get_json())

    def testInvalidLogin(self):
        """Testing for invalid user login"""
        response = self.app.post('/auth/login', json={
            "email": "invalid@example.com",
            "password": "wrongpwd"
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid credentials', response.get_json()["error"])