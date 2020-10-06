from . import db

class DF_World(db.Model):
    __tablename__ = 'df_world'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    altname = db.Column(db.String(50))
    height_pixels = db.Column(db.Integer)
    width_pixels = db.Column(db.Integer)
    height_coords = db.Column(db.Integer)
    width_coords = db.Column(db.Integer)

    historical_figures = db.relationship('Historical_Figure', backref='df_world')
    artifacts = db.relationship('Artifact', backref='df_world')
    historical_eras = db.relationship('Historical_Era', backref='df_world')

    def __repr__(self):
        return "<df_world %s>" % (id)
