#!/usr/bin/python3
""" eCity """
from ecity.app.routes import app, db


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    print('** Changes Saved.')
