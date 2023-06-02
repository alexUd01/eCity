#!/usr/bin/python3
""" eCity """
from ecity.app.routes import app, db


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        db = db.session()
        # db.add_all([person1, person2])
        app.run(host='0.0.0.0', port=5000, debug=True)
        db.commit()
