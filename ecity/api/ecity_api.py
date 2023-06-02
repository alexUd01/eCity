#!/usr/bin/python3
"""API for eCity"""
from flask import Flask

e_api = Flask(__name__)


@e_api.route('/api', strict_slashes=False)
def api():
    """Returns API Status"""
    return '{"Status": "OK"}\n'


if __name__ == "__main__":
    e_api.run(host='0.0.0.0', port='5001', debug=True)
