from . import db
from .join_builder import join_builder as jb, table_join_builder as tjb

# Civs and Local Govts

class Entity(db.Model):
    __tablename__ = 'entities'
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'),
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    race = db.Column(db.String(20))
    type = db.Column(db.String(20))
    claims = db.Column(db.String)
    worship_id = db.Column(db.Integer)

    #site_links = db.relationship('Site_Link', backref='entity', 
    #                             viewonly=True)
    site_links = db.relationship('Site_Link', backref='entity', 
                                 viewonly=True, 
                                 foreign_keys="Site_Link.df_world_id,"
                                              "Site_Link.entity_id",
                                 primaryjoin=jb('Entity', 'Site_Link', 
                                               ('id', 'entity_id')))
    
    sites = db.relationship('Site', backref='entity',
                    viewonly=True, foreign_keys="Site.df_world_id, Site.civ_id",
                    primaryjoin=jb('Entity', 'Site', ('id', 'civ_id')))
    local_sites = db.relationship('Site', backref='local_entity',
                viewonly=True, foreign_keys="Site.df_world_id, Site.current_owner_id",
                primaryjoin=jb('Entity', 'Site', ('id', 'current_owner_id')))
    structures = db.relationship('Structure', backref='entity',
                                 viewonly=True, 
                                 foreign_keys="Structure.df_world_id,"
                                              "Structure.entity_id",
                                 primaryjoin=jb('Entity', 'Structure',
                                                ('id', 'entity_id')))

    entity_position_links = db.relationship('Entity_Position_Link',
                                backref='entity',
                                viewonly=True, 
                                foreign_keys="Entity_Position_Link.df_world_id,"
                                             "Entity_Position_Link.entity_id",
                                primaryjoin=jb('Entity', 'Entity_Position_Link',
                                    ('id', 'entity_id')))
    entity_reputations = db.relationship('Entity_Reputation',
                             backref='entity',
                             viewonly=True, 
                             foreign_keys="Entity_Reputation.df_world_id,"
                                          "Entity_Reputation.entity_id",
                             primaryjoin=jb('Entity', 'Entity_Reputation',
                                    ('id', 'entity_id')))
    entity_links =  db.relationship('Entity_Link',
                             backref='entity',
                             viewonly=True, 
                             foreign_keys="Entity_Link.df_world_id,"
                                          "Entity_Link.entity_id",
                             primaryjoin=jb('Entity', 'Entity_Link',
                                    ('id', 'entity_id')))

    positions = db.relationship("Entity_Position",
            backref='entity', viewonly=True,
            foreign_keys="Entity_Position.df_world_id,"
                         "Entity_Position.entity_id",
            primaryjoin=jb("Entity", "Entity_Position",
                           ('id', 'entity_id')))

    eventcols1 = db.relationship('Event_Collection', backref='entity1', 
                                foreign_keys="Event_Collection.entity_id,"
                                             "Event_Collection.df_world_id",
                                primaryjoin=jb('Entity', 'Event_Collection',
                                    ('id', 'entity_id')))
    eventcols2 = db.relationship('Event_Collection', backref='entity2', 
                                foreign_keys="Event_Collection.entity_id,"
                                             "Event_Collection.df_world_id",
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
                    foreign_keys="Historical_Event.df_world_id,"
                                 "Historical_Event.entity_id", 
                    uselist=True, 
                    viewonly=True)

    sec_events = db.relationship('Historical_Event', backref='entity_2', 
                    primaryjoin='and_(Historical_Event.entity_id2 == ' +
                                        'Entity.id,' +
                                      'Historical_Event.df_world_id == ' +
                                         'Entity.df_world_id)',
                    uselist=True,
                    foreign_keys="Historical_Event.df_world_id,"
                                 "Historical_Event.entity_id2", 
                    viewonly=True)

    site_civ_events = db.relationship('Historical_Event', 
                                      backref='site_civ', 
                    primaryjoin='and_(Historical_Event.site_civ_id == ' +
                                        'Entity.id,' +
                                      'Historical_Event.df_world_id == ' +
                                         'Entity.df_world_id)',
                    uselist=True, 
                    foreign_keys="Historical_Event.df_world_id,"
                                 "Historical_Event.site_civ_id", 
                    viewonly=True)
    
    new_site_civ_events = db.relationship('Historical_Event', 
                                      backref='new_site_civ', 
        primaryjoin='and_(Historical_Event.new_site_civ_id == ' +
                                        'Entity.id,' +
                                      'Historical_Event.df_world_id == ' +
                                         'Entity.df_world_id)',
        foreign_keys="Historical_Event.df_world_id,"
                     "Historical_Event.new_site_civ_id", 
        uselist=True, 
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
                    foreign_keys="Historical_Event.df_world_id,"
                                 "Historical_Event.new_site_civ_id,"
                                 "Historical_Event.site_civ_id,"
                                 "Historical_Event.entity_id,"
                                 "Historical_Event.entity_id2", 
                    uselist=True,
                    viewonly=True)

    populations = db.relationship('Entity_Population',
            backref='entity', viewonly=True, 
            foreign_keys="Entity_Population.df_world_id,"
                         "Entity_Population.civ_id",
            primaryjoin=jb("Entity", "Entity_Population", ("id", "civ_id")))

    entity_links_out = db.relationship('Entity_Entity_Link',
            backref='back_entity', viewonly=True,
            foreign_keys="Entity_Entity_Link.df_world_id,"
                         "Entity_Entity_Link.entity_id",
            primaryjoin=jb("Entity", "Entity_Entity_Link", ("id", "entity_id")))
    entity_links_in = db.relationship('Entity_Entity_Link',
            backref='forward_entity', viewonly=True,
            foreign_keys="Entity_Entity_Link.df_world_id,"
                         "Entity_Entity_Link.target",
            primaryjoin=jb("Entity", "Entity_Entity_Link", ("id", "target")))
    occasions = db.relationship('Occasion',
            backref='entity', viewonly=True,
            foreign_keys="Occasion.df_world_id, Occasion.entity_id",
            primaryjoin=jb("Entity", "Occasion", ("id", "entity_id")))



class Entity_Population(db.Model):
    __tablename__ = 'entity_populations'

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    race = db.Column(db.String(20))
    civ_id = db.Column(db.Integer)
    num = db.Column(db.Integer)

# Details on Entity from extended 

class Occasion(db.Model):
    __tablename__ = 'occasions'
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'),
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    event = db.Column(db.Integer)

    schedules = db.relationship('Schedule',
            backref='occasion', viewonly=True,
            foreign_keys="Schedule.df_world_id, "
                         "Schedule.entity_id, Schedule.occasion_id",
            primaryjoin=jb("Occasion", "Schedule", 
                           ("id", "occasion_id"), ("entity_id", "entity_id")))

class Schedule(db.Model):
    __tablename__ = 'schedules'
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'),
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)

    occasion_id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer, primary_key=True)

    type = db.Column(db.String(30))
    reference = db.Column(db.Integer)
    reference2 = db.Column(db.Integer)
    item_type = db.Column(db.String(30))
    item_subtype = db.Column(db.String(30))

    features = db.relationship('Feature', backref='schedule', viewonly=True,
            foreign_keys="Feature.df_world_id, Feature.entity_id,"
                         "Feature.occasion_id, Feature.schedule_id",
            primaryjoin=jb("Schedule", "Feature", ("id", "schedule_id"),
                 ("occasion_id", "occasion_id"), ("entity_id", "entity_id")))


class Feature(db.Model):
    __tablename__ = 'features'
    df_world_id = db.Column(db.Integer, 
                      db.ForeignKey('df_world.id', ondelete='CASCADE'))
    id = db.Column(db.Integer, primary_key=True)
    occasion_id = db.Column(db.Integer)
    schedule_id = db.Column(db.Integer)
    entity_id = db.Column(db.Integer)
    
    type = db.Column(db.String(30))
    reference = db.Column(db.Integer)

class Entity_Position(db.Model):
    __tablename__ = 'entity_positions'
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'),
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    name_male = db.Column(db.String(20))
    name_female = db.Column(db.String(20))
    spouse_male = db.Column(db.String(20))
    spouse_female = db.Column(db.String(20))

    holder = db.relationship("Entity_Position_Assignment",
            viewonly=True, backref="position", uselist=False,
            foreign_keys="Entity_Position_Assignment.df_world_id,"
                         "Entity_Position_Assignment.entity_id,"
                         "Entity_Position_Assignment.position_id",
            primaryjoin=jb("Entity_Position", "Entity_Position_Assignment",
                ("entity_id", "entity_id"), ("id", "position_id")))

    def calculated_name(self):
        if (self.holder and self.name_female 
                        and not self.holder.histfig == -1 
                        and self.holder.hf.caste == 'FEMALE'):
            return self.name_female
        return self.name


class Entity_Position_Assignment(db.Model):
    __tablename__ = 'entity_position_assignments'
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'),
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer, primary_key=True)
    histfig = db.Column(db.Integer)
    position_id = db.Column(db.Integer)
    squad_id = db.Column(db.Integer)


class Entity_Entity_Link(db.Model):
    __tablename__ = 'entity_entity_links'
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', 
                                                      ondelete='CASCADE'))
    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer)
    type = db.Column(db.String(50))
    target = db.Column(db.Integer)
    strength = db.Column(db.Integer)

## Sites and Structures

class Site(db.Model):
    __tablename__ = 'sites'

    types = ['cave', 'fortress', 'dark fortress', 'forest retreat',
             'town', 'vault', 'hillocks', 'dark pits', 'hamlet',
            'tomb', 'mountain halls', 'camp', 'lair', 'shrine', 'tower']

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    coords = db.Column(db.String(10))
    rectangle = db.Column(db.String(20))
    type = db.Column(db.Enum(*types, name='site_types'))

    civ_id = db.Column(db.Integer)
    current_owner_id = db.Column(db.Integer)

    site_links = db.relationship('Site_Link', backref='site', 
                                 viewonly=True,
                                 foreign_keys="Site_Link.df_world_id,"
                                              "Site_Link.id",
                                 primaryjoin=jb('Site', 
                                                'Site_Link', 
                                               ('id', 'site_id')))

    structures = db.relationship('Structure', backref='site', viewonly=True,
                                 foreign_keys="Structure.df_world_id,"
                                              "Structure.site_id",
                                 primaryjoin=jb('Site', 'Structure', 
                                                ('id', 'site_id')))
    event_collections = db.relationship('Event_Collection', backref='site',
                                        viewonly=True, 
                                        foreign_keys="Event_Collection.df_world_id,"
                                                     "Event_Collection.site_id",
                                 primaryjoin=jb('Site', 'Event_Collection', 
                                                ('id', 'site_id')))
    
    stored_artifacts = db.relationship('Artifact', backref='storage_site', 
                                       primaryjoin=jb('Site', 'Artifact',
                                                      ('id', 'site_id')),
                                       foreign_keys="Artifact.df_world_id,"
                                                    "Artifact.site_id",
                                       viewonly=True)
    
    prim_events = db.relationship('Historical_Event', backref='site', 
                    primaryjoin='and_(Historical_Event.site_id == ' +
                                        'Site.id,' +
                                      'Historical_Event.df_world_id == ' +
                                         'Site.df_world_id)',
                    foreign_keys="Historical_Event.df_world_id,"
                                 "Historical_Event.site_id",
                    uselist=True, 
                    viewonly=True)

    sec_events = db.relationship('Historical_Event', backref='site_2', 
                    primaryjoin='and_(Historical_Event.site_id2 == ' +
                                        'Site.id,' +
                                      'Historical_Event.df_world_id == ' +
                                         'Site.df_world_id)',
                    foreign_keys="Historical_Event.df_world_id,"
                                 "Historical_Event.site_id2",
                    uselist=True,
                    viewonly=True)
    
    all_events = db.relationship('Historical_Event', 
                    primaryjoin='and_(' +
                                   'or_(Historical_Event.site_id == ' +
                                        'Site.id,' +
                                   'Historical_Event.site_id2 == ' +
                                        'Site.id),' +
                                      'Historical_Event.df_world_id == ' +
                                         'Site.df_world_id)',
                    foreign_keys="Historical_Event.df_world_id,"
                                 "Historical_Event.site_id,"
                                 "Historical_Event.site_id2",
                    uselist=True,
                    viewonly=True)

class Structure(db.Model):
    __tablename__ = 'structures'

    types = ['underworld spire', 'inn tavern', 'market', 'temple',
             'dungeon', 'keep', 'tomb', 'mead hall', 'library']
    subtypes = ['catacombs', 'standard', 'sewers']
    
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'), 
                            primary_key=True)
    site_id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer)
    local_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    name2 = db.Column(db.String(50))
    type = db.Column(db.Enum(*types, name='structure_types'))
    subtype = db.Column(db.Enum(*subtypes, name='structure_subtypes'))
    worship_hfid = db.Column(db.Integer)

    inhabitants = db.relationship('Historical_Figure',
                                     backref='home_structure',
                                     secondary='inhabitants',
                                     viewonly=True,
                              primaryjoin=tjb('Structure', 'inhabitants', 
                                            ('local_id', 'structure_id'), 
                                            ('site_id', 'site_id')),
                              secondaryjoin=tjb('Historical_Figure', 'inhabitants', 
                                             ('id', 'hfid')))

# Intermediate tables

members = db.Table('members', db.metadata,
        db.Column('id', db.Integer,  primary_key=True),
        db.Column('df_world_id', db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE')),
        db.Column('entity_id', db.Integer),
        db.Column('hfid', db.Integer),
        )

inhabitants = db.Table('inhabitants', db.metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('df_world_id', db.Integer,  db.ForeignKey('df_world.id', ondelete='CASCADE')),
        db.Column('site_id', db.Integer),
        db.Column('structure_id', db.Integer),
        db.Column('hfid', db.Integer),
        )

class Site_Map(db.Model):
    __tablename__ = 'site_maps'
    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', 
                                                      ondelete='CASCADE'))
    site_id = db.Column(db.Integer)
    path = db.Column(db.String(80))
