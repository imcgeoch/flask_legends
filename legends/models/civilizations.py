from . import db
from .join_builder import join_builder as jb, table_join_builder as tjb

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

    #site_links = db.relationship('Site_Link', backref='entity', 
    #                             viewonly=True)
    site_links = db.relationship('Site_Link', backref='entity', 
                                 viewonly=True, foreign_keys=[id, df_world_id],
                                 primaryjoin=jb('Entity', 'Site_Link', 
                                               ('id', 'entity_id')))
    structures = db.relationship('Structure', backref='entity',
                                 viewonly=True, foreign_keys=[id, df_world_id],
                                 primaryjoin=jb('Entity', 'Structure',
                                                ('id', 'entity_id')))

    entity_position_links = db.relationship('Entity_Position_Link',
                                backref='entity',
                                viewonly=True, foreign_keys=[id, df_world_id],
                                primaryjoin=jb('Entity', 'Entity_Position_Link',
                                    ('id', 'entity_id')))
    entity_reputations = db.relationship('Entity_Reputation',
                             backref='entity',
                             viewonly=True, foreign_keys=[id, df_world_id],
                             primaryjoin=jb('Entity', 'Entity_Reputation',
                                    ('id', 'entity_id')))
    entity_links =  db.relationship('Entity_Link',
                             backref='entity',
                             viewonly=True, foreign_keys=[id, df_world_id],
                             primaryjoin=jb('Entity', 'Entity_Link',
                                    ('id', 'entity_id')))

    eventcols1 = db.relationship('Event_Collection', backref='entity1', 
                                foreign_keys=[id, df_world_id],
                                primaryjoin=jb('Entity', 'Event_Collection',
                                    ('id', 'entity_id')))
    eventcols2 = db.relationship('Event_Collection', backref='entity2', 
                                foreign_keys=[id, df_world_id],
                                primaryjoin=jb('Entity', 'Event_Collection',
                                    ('id', 'entity_id2')))
    members = db.relationship('Historical_Figure',
                                     backref='member_of',
                                     secondary='members',
                                     viewonly=True,
                              primaryjoin=tjb('Entity', 'members', 
                                            ('id', 'entity_id')),
                              secondaryjoin=tjb('Historical_Figure', 'members', 
                                             ('id', 'hfid')))
    
    prim_events = db.relationship('Historical_Event', backref='entity', 
                    primaryjoin='and_(Historical_Event.entity_id == ' +
                                        'Entity.id,' +
                                      'Historical_Event.df_world_id == ' +
                                         'Entity.df_world_id)',
                    foreign_keys=[id, df_world_id], uselist=True, 
                    viewonly=True)

    sec_events = db.relationship('Historical_Event', backref='entity_2', 
                    primaryjoin='and_(Historical_Event.entity_id2 == ' +
                                        'Entity.id,' +
                                      'Historical_Event.df_world_id == ' +
                                         'Entity.df_world_id)',
                    foreign_keys=[id, df_world_id], uselist=True,
                    viewonly=True)

    site_civ_events = db.relationship('Historical_Event', 
                                      backref='site_civ', 
                    primaryjoin='and_(Historical_Event.site_civ_id == ' +
                                        'Entity.id,' +
                                      'Historical_Event.df_world_id == ' +
                                         'Entity.df_world_id)',
                    foreign_keys=[id, df_world_id], uselist=True, 
                    viewonly=True)
    
    new_site_civ_events = db.relationship('Historical_Event', 
                                      backref='new_site_civ', 
        primaryjoin='and_(Historical_Event.new_site_civ_id == ' +
                                        'Entity.id,' +
                                      'Historical_Event.df_world_id == ' +
                                         'Entity.df_world_id)',
        foreign_keys=[id, df_world_id], uselist=True, 
        viewonly=True)
    
    all_events = db.relationship('Historical_Event', 
                    primaryjoin='and_(' +
                                   'or_(Historical_Event.entity_id == ' +
                                        'Entity.id,' +
                                   'Historical_Event.entity_id2 == ' +
                                        'Entity.id,' +
                                   'Historical_Event.site_civ_id == ' +
                                        'Entity.id,' +
                                   'Historical_Event.new_site_civ_id == ' +
                                        'Entity.id),' +
                                      'Historical_Event.df_world_id == ' +
                                         'Entity.df_world_id)',
                    foreign_keys=[id, df_world_id], uselist=True,
                    viewonly=True)

class Entity_Population(db.Model):
    __tablename__ = 'entity_populations'

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    race = db.Column(db.String(20))
    civ_id = db.Column(db.Integer)
    num = db.Column(db.Integer)

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
    type = db.Column(db.Enum(*types, name='site_types'))

    civ_id = db.Column(db.Integer)
    current_owner_id = db.Column(db.Integer)

    site_links = db.relationship('Site_Link', backref='site', 
                                 viewonly=True, foreign_keys=[id, df_world_id],
                                 primaryjoin=jb('Site', 
                                                'Site_Link', 
                                               ('id', 'site_id')))

    structures = db.relationship('Structure', backref='site', viewonly=True,
                                 foreign_keys=[id, df_world_id],
                                 primaryjoin=jb('Site', 'Structure', 
                                                ('id', 'site_id')))
    event_collections = db.relationship('Event_Collection', backref='site',
                                        viewonly=True)
    
    stored_artifacts = db.relationship('Artifact', backref='storage_site', 
                                       primaryjoin='and_(Artifact.site_id == '+
                                                         'Site.id,' +
                                                         'Artifact.df_world_id ==' +
                                                         'Site.df_world_id)',
                                     foreign_keys=[id, df_world_id],
                                      viewonly=True)
    
    prim_events = db.relationship('Historical_Event', backref='site', 
                    primaryjoin='and_(Historical_Event.site_id == ' +
                                        'Site.id,' +
                                      'Historical_Event.df_world_id == ' +
                                         'Site.df_world_id)',
                    foreign_keys=[id, df_world_id], uselist=True, 
                    viewonly=True)

    sec_events = db.relationship('Historical_Event', backref='site_2', 
                    primaryjoin='and_(Historical_Event.site_id2 == ' +
                                        'Site.id,' +
                                      'Historical_Event.df_world_id == ' +
                                         'Site.df_world_id)',
                    foreign_keys=[id, df_world_id], uselist=True,
                    viewonly=True)
    
    all_events = db.relationship('Historical_Event', 
                    primaryjoin='and_(' +
                                   'or_(Historical_Event.site_id == ' +
                                        'Site.id,' +
                                   'Historical_Event.site_id2 == ' +
                                        'Site.id),' +
                                      'Historical_Event.df_world_id == ' +
                                         'Site.df_world_id)',
                    foreign_keys=[id, df_world_id], uselist=True,
                    viewonly=True)

class Structure(db.Model):
    __tablename__ = 'structures'

    types = ['underworld spire', 'inn tavern', 'market', 'temple',
             'dungeon', 'keep', 'tomb', 'mead hall', 'library']
    subtypes = ['catacombs', 'standard', 'sewers']
    
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'), 
                            primary_key=True)
    site_id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer)
    local_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    name2 = db.Column(db.String(50))
    type = db.Column(db.Enum(*types, name='structure_types'))
    subtype = db.Column(db.Enum(*subtypes, name='structure_subtypes'))
    worship_hfid = db.Column(db.Integer)

# Intermediate tables

members = db.Table('members', db.metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('df_world_id', db.Integer),
        db.Column('entity_id', db.Integer),
        db.Column('hfid', db.Integer),
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

