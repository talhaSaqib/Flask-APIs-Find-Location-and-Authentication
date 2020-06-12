# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mongoengine import *
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


AUTH_SECRET_KEY = "a_=hf+n&4y6z5gw9ogrt6y9utnbog9n+f8k1s28fbnyrg75!t_ge^"

class ApiAuth(Document):
    username = StringField(max_length=32)
    password = StringField()
    password_hash = StringField()

    def hash_password(self, password):
        try:
            self.password_hash = generate_password_hash(password)
        except Exception as e:
            print(e)


    def generate_auth_token(self, expiration=600):
        try:
            s = Serializer(AUTH_SECRET_KEY, expires_in=expiration)
            return s.dumps({'id': str(self.id)})
        except Exception as e:
            print(e)

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(AUTH_SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token

        user = ApiAuth.objects.get(data['id'])
        return user