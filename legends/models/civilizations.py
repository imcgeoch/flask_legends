from . import db

# Civs and Local Govts

class Entity(db.Model):
    __tablename__ = 'entities'
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'),
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    race = db.Column(db.String(20))
    type = db.Column(db.String(20))
    claims = db.Column(db.String)

    site_links = db.relationship('Site_Link', backref='entity', 
                                 viewonly=True)
    structures = db.relationship('Structure', backref='entity',
                                 viewonly=True)
    entity_position_links = db.relationship('Entity_Position_Link',
                                backref='entity',
                                viewonly=True)
    entity_reputations = db.relationship('Entity_Reputation',
                             backref='entity',
                             viewonly=True)
    eventcols1 = db.relationship('Event_Collection', 
                                backref='entity1', 
                                foreign_keys='Event_Collection.entity_id,'
                                            'Event_Collection.df_world_id')
    eventcols2 = db.relationship('Event_Collection', 
                                backref='entity2', 
                                foreign_keys='Event_Collection.entity_id2,'
                                       'Event_Collection.df_world_id')
    members = db.relationship('Historical_Figure',
                                     backref='member_of',
                                     secondary='members',
                                     viewonly=True)

# Details on Entity from extended 

class Occasion(db.Model):
    __tablename__ = 'occasions'
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'),
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer)

    name = db.Column(db.String(50))
    event = db.Column(db.Integer)

class Schedules(db.Model):
    __tablename__ = 'schedules'
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'),
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)

    occasion_id = db.Column(db.Integer)
    entity_id = db.Column(db.Integer)

    type = db.Column(db.String(20))
    reference = db.Column(db.Integer)
    reference2 = db.Column(db.Integer)
    item_type = db.Column(db.String(20))
    item_subtype = db.Column(db.String(20))

class Features(db.Model):
    __tablename__ = 'features'
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'),
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    occasion_id = db.Column(db.Integer)
    schedule_id = db.Column(db.Integer)
    entity_id = db.Column(db.Integer)
    
    type = db.Column(db.String(20))
    reference = db.Column(db.Integer)

class Entity_Position(db.Model):
    __tablename__ = 'entity_positions'
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'),
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer)
    name = db.Column(db.String(20))
    name_male = db.Column(db.String(20))
    name_female = db.Column(db.String(20))
    spouse_male = db.Column(db.String(20))
    spouse_female = db.Column(db.String(20))

## Sites and Structures

class Site(db.Model):
    __tablename__ = 'sites'

    types = ['cave', 'fortress', 'dark fortress', 'forest retreat',
             'town', 'vault', 'hillocks', 'dark pits', 'hamlet',
            'tomb', 'mountain halls', 'camp', 'lair', 'shrine']

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    coords = db.Column(db.String(10))
    rectangle = db.Column(db.String(20))
    type = db.Column(db.Enum(*types))

    civ_id = db.Column(db.Integer)
    current_owner_id = db.Column(db.Integer)

    site_links = db.relationship('Site_Link', backref='site', viewonly=True)
    structures = db.relationship('Structure', backref='site', viewonly=True)
    event_collections = db.relationship('Event_Collection', backref='site',
                                        viewonly=True)

class Structure(db.Model):
    __tablename__ = 'structures'

    types = ['underworld spire', 'inn tavern', 'market', 'temple',
             'dungeon', 'keep', 'tomb', 'mead hall', 'library']
    subtypes = ['catacombs', 'standard']
    
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'), 
                            primary_key=True)
    site_id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer, primary_key=True)
    local_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    name2 = db.Column(db.String(50))
    type = db.Column(db.Enum(*types))
    subtype = db.Column(db.Enum(*subtypes))
    worship_hfid = db.Column(db.Integer)

    #inhabitants redundant?

    __table_args__ = (db.ForeignKeyConstraint([df_world_id, site_id],
                                 [Site.df_world_id, Site.id]),
                      db.ForeignKeyConstraint([df_world_id, entity_id],
                                 [Entity.df_world_id, Entity.id]),
                      db.ForeignKeyConstraint([df_world_id, worship_hfid],
                                 ['historical_figures.df_world_id',
                                  'historical_figures.id']), {})

# Intermediate tables

members = db.Table('members', db.metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('df_world_id', db.Integer),
        db.Column('entity_id', db.Integer),
        db.Column('hfid', db.Integer),
        db.ForeignKeyConstraint(['df_world_id', 'hfid'],
                                ['historical_figures.df_world_id',
                                 'historical_figures.id']),
        db.ForeignKeyConstraint(['df_world_id', 'entity_id'],
                                ['entities.df_world_id', 
                                 'entities.id'])
        )

inhabitants = db.Table('inhabitants', db.metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('df_world_id', db.Integer),
        db.Column('site_id', db.Integer),
        db.Column('structure_id', db.Integer),
        db.Column('hfid', db.Integer),
        db.ForeignKeyConstraint(['df_world_id', 'hfid'],
                                ['historical_figures.df_world_id',
                                 'historical_figures.id']),
        db.ForeignKeyConstraint(['df_world_id', 'site_id', 'structure_id'],
                                ['structures.df_world_id', 
                                 'structures.site_id',
                                 'structures.local_id'])
        )
