# -*- coding: utf-8 -*-

import unittest
from app.models import User


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u1 = User(password='cat')
        u2 = User(password='cat')
        self.assertFalse(u1.password_hash == u2.password_hash)

    def test_confirmation_token_salts_are_random(self):
        u = User()
        token1 = u.generate_confirmation_token()
        token2 = u.generate_confirmation_token()
        self.assertFalse(token1 == token2)

    def test_confirm(self):
        u = User()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))