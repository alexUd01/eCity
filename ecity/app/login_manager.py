#!/usr/bin/env python3
"""
Login manager module
"""
import flask_login
from flask_login import LoginManager, logout_user, login_required, login_user
from flask_login import login_remembered
from datetime import timedelta

lm = LoginManager()
print(dir(flask_login.config))
print(flask_login.config.SESSION_KEYS)
