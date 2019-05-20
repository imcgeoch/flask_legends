import unittest
import flask_testing

from flask_testing import TestCase

from legends import create_app
from legends.models import db, DF_World

class MyTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.create_all()
        w = DF_World(id=1, name="The Tested Realm")
        db.session.add(w)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_dumb(self):
        assert True

    def test_world_exists(self):
        world = DF_World.query.first()
        assert world.id == 1




if __name__ == '__main__':
    unittest.main()
