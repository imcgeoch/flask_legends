from . import db

class Landmass(db.Model):
    __tablename__ = 'landmasses'
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'),
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    coord1 = db.Column(db.String(10))
    coord2 = db.Column(db.String(10))

class Mountain_Peak(db.Model):
    __tablename__ = 'mountain_peaks'
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'),
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)

    coords = db.Column(db.String(10))
    height = db.Column(db.Integer)

class Region(db.Model):
    __tablename__ = 'regions'

    types = ['Wetland', 'Grassland', 'Hills', 'Desert', 'Forest',
             'Mountains', 'Lake', 'Ocean', 'Tundra', 'Glacier']

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    type = db.Column(db.Enum(*types, name='region_types'))
    coords = db.Column(db.String)
    
    events = db.relationship('Historical_Event', backref='region', 
                    primaryjoin='and_(Historical_Event.subregion_id == ' +
                                        'Region.id,' +
                                      'Historical_Event.df_world_id == ' +
                                         'Region.df_world_id)',
                    foreign_keys="Historical_Event.df_world_id,"
                                 "Historical_Event.subregion_id")

class Underground_Region(db.Model):
    __tablename__ = 'underground_regions'

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum('cavern', 'magma', 'underworld', name='ug_region_types'))
    coords = db.Column(db.String)

class World_Construction(db.Model):
    __tablename__ = 'world_constructions'
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    type = db.Column(db.String(50)) #should be enum
    coords = db.Column(db.String)

class River(db.Model):
    __tablename__ = 'rivers'
    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer, 
                            db.ForeignKey('df_world.id', ondelete='CASCADE'))
    name = db.Column(db.String(100))
    path = db.Column(db.String)
    end_pos = db.Column(db.String(12))

class Creature(db.Model):
    __tablename__ = 'creatures'
    creature_id = db.Column(db.String(30), primary_key=True)
    df_world_id = db.Column(db.Integer, 
                            db.ForeignKey('df_world.id', ondelete='CASCADE'))
    name_singular = db.Column(db.String(30))
    name_plural = db.Column(db.String(30))

class World_Map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'world_maps'
    df_world_id = db.Column(db.Integer, 
                            db.ForeignKey('df_world.id', ondelete='CASCADE'))

    map_types = ['bm', 'detailed', 'dip', 'drn', 'el', 'elw', 'evil', 'hyd',
                 'nob', 'rain', 'sal', 'sav', 'str', 'tmp', 'trd', 'veg',
                 'vol', 'world_map']
    type = db.Column(db.Enum(*map_types, name="map_types"))
    path = db.Column(db.String(80)) 
