# -*- coding: utf-8 -*-
from __future__ import unicode_literals 
import os
import sys
from time import sleep
import logging
import json
from flask import Flask, jsonify, abort, make_response, request, g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.security import generate_password_hash, check_password_hash
from FlaskAPI.connection import *

# /pathto/fnb-backend
root_dir = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(root_dir)
# print "root_dir > ",root_dir
logging.basicConfig(
    format='[%(asctime)s > %(module)s:%(lineno)d %(levelname)s]:%(message)s',
    level=logging.INFO,
    datefmt='%m/%d/%Y %I:%M:%S %p'
)
logger = logging.getLogger(__name__)
auth = HTTPBasicAuth()
# token_auth = HTTPTokenAuth(scheme="Token")

@auth.verify_password
def verify_password_call(username_or_token, password):

    user = ApiAuth.verify_auth_token(username_or_token)
    if not user:
        logger.info("Token invalid! Now checking username and password")
        try:
            user = ApiAuth.objects.get(username=username_or_token)

            if check_password_hash(user.password_hash, password) is True:
                user['id'] = str(user['id'])
                g.user = user
                return g.user
            else:
                return False
        except ApiAuth.DoesNotExist:
            return False
    else:
        return user

# NOT BEING USED
# @token_auth.verify_token
# def verify_token(token):
#     try:
#         user = ApiAuth.verify_auth_token(token)
#         if user:
#             return user
#         else:
#             return False
#
#     except Exception as e:
#         return False


def new_api_user(username, password):
    if username is None or password is None:
        logger.error("'username' and 'password' is None .")
        return
    try:
        ApiAuth.objects.get(username=username)
        logger.error("username:'{}' already exists".format(username))
        return
    except ApiAuth.DoesNotExist:
        user = ApiAuth(username=username)
        user.hash_password(password)
        user.save()
        logging.info("<new_user> created:{}".format(user.username))
    return user


if __name__ == '__main__':
    # print dump_record_by_fieldNames(collection_name = "Customer", customerEmail = 'None')
    user = new_api_user('admin', 'FunnelBeam123')
    user = new_api_user('asad', 'alaska8k21')
# print verify_password('admin','FunnelBeam123')
# pwd = 'asad'
# pwd_hash = generate_password_hash(u'asad')
# print "pwd is >'{}'".format(pwd)
# print "pwd_hash is >'{}'".format(pwd_hash)
# print check_password_hash(pwd_hash, pwd)
