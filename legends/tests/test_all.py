import unittest
import flask_testing

from flask_testing import TestCase

from legends import create_app
from legends.models import db, Artifact, DF_World, Historical_Figure, \
                           Historical_Era

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
        a1 = Artifact(df_world_id=1, id=1, name="a big axe")
        a2 = Artifact(df_world_id=1, id=2, name="a big book", holder_hfid=1)
        hf1 = Historical_Figure(df_world_id=1, id=1)
        db.session.add(a1)
        db.session.add(a2)
        db.session.add(hf1)
        he1 = Historical_Era(df_world_id=1, name="the time of trials", 
                             start_year=15)
        db.session.add(he1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_dumb(self):
        assert True

    def test_world_exists(self):
        world = DF_World.query.first()
        assert world.id == 1
        assert world.name == "The Tested Realm"

    def test_artifacts_in_world(self):
        world = DF_World.query.first()
        a1 = Artifact.query.get((1,1))
        a2 = Artifact.query.get((1,2))
        assert world.artifacts == [a1, a2] 

    def test_hf_holds_artifact(self):
        hf = Historical_Figure.query.get((1,1))
        a2 = Artifact.query.get((1,2))
        assert hf.held_artifacts == [a2]

    def test_artifact_repr(self):
        a2 = Artifact.query.get((1,2))
        assert repr(a2) == '<Artifact a big book>'

    def test_era_in_world(self):
        world = DF_World.query.first()
        he = Historical_Era.query.get((1, "the time of trials"))
        assert world.historical_eras == [he]

    def test_era_repr(self):
        he = Historical_Era.query.get((1, "the time of trials"))
        assert repr(he) == '<Historical Era the time of trials>'






if __name__ == '__main__':
    unittest.main()
