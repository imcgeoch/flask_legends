from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

competitors = db.Table('competitors', db.metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('df_world_id', db.Integer),
        db.Column('event_id', db.Integer),
        db.Column('competitor_hfid', db.Integer),
        db.ForeignKeyConstraint(['df_world_id', 'competitor_hfid'],
                                ['historical_figures.df_world_id',
                                 'historical_figures.id']),
        db.ForeignKeyConstraint(['df_world_id', 'event_id'],
                                ['historical_events.df_world_id',
                                 'historical_events.id'])
        )

entity_position_links = db.Table('entity_position_links', db.metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('df_world_id', db.Integer),
        db.Column('hfid', db.Integer),
        db.Column('entity_id', db.Integer),
        db.Column('start_year', db.Integer),
        db.Column('end_year', db.Integer),
        db.Column('position_profile_id', db.Integer),
        
        db.ForeignKeyConstraint(['df_world_id', 'hfid'],
                                ['historical_figures.df_world_id',
                                 'historical_figures.id']),
        db.ForeignKeyConstraint(['df_world_id', 'entity_id'],
                                ['entities.df_world_id', 'entities.id'])
        )

entity_reputations = db.Table('entity_reputations', db.metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('df_world_id', db.Integer),
        db.Column('hfid', db.Integer),
        db.Column('entity_id', db.Integer),
        db.Column('first_ageless_season_count', db.Integer),
        db.Column('first_ageless_year', db.Integer),
        db.Column('unsolved_murders', db.Integer),
        
        db.ForeignKeyConstraint(['df_world_id', 'hfid'],
                                ['historical_figures.df_world_id',
                                 'historical_figures.id']),
        db.ForeignKeyConstraint(['df_world_id', 'entity_id'],
                                ['entities.df_world_id', 'entities.id'])
        )



class DF_World(db.Model):
    __tablename__ = 'df_world'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    historical_figures = db.relationship('Historical_Figure', backref='df_world')
    artifacts = db.relationship('Artifact', backref='df_world')
    historical_eras = db.relationship('Historical_Era', backref='df_world')

    def __repr__(self):
        return "<df_world %s>" % (id)

class Dance_Form(db.Model):
    __tablename__ = 'dance_forms'
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'),
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text())

class Entity(db.Model):
    __tablename__ = 'entities'
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'),
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))


class Historical_Figure(db.Model):
    __tablename__ = 'historical_figures'

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'),
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    race = db.Column(db.String(20))
    caste = db.Column(db.String(10))
    deity = db.Column(db.Boolean) # Self-closing in xml
    force = db.Column(db.Boolean) # Self-closing in xml
    active_interaction = db.Column(db.String(50)) # Ex: DEITY_FORCE_WAREB...
    animated = db.Column(db.Boolean)
    animated_string = db.Column(db.String(50))
    appeared = db.Column(db.Integer) # a year
    associated_type = db.Column(db.String(20)) #Ex: BOWMAN
    birth_seconds72 = db.Column(db.Integer) 
    birth_year = db.Column(db.Integer)
    death_seconds72 = db.Column(db.Integer)
    death_year = db.Column(db.Integer)
    current_identity_id = db.Column(db.Integer)
    ent_pop_id = db.Column(db.Integer)

    held_artifacts = db.relationship('Artifact', backref='holder_hf', 
                                      viewonly=True)

    competitions = db.relationship('Historical_Event', 
                          secondary='competitors',
                          backref='competitors', 
                          viewonly=True)
    entity_position_links = db.relationship('Entity', 
                                secondary='entity_position_links',
                                backref='position_holders',
                                viewonly=True)
    entity_reputations = db.relationship('Entity',
                             secondary='entity_reputations',
                             backref='reputation_holders',
                             viewonly=True)

    def __repr__(self):
        return "<Historical Figure %s>" % (self.name)

class Artifact(db.Model):
    __tablename__ = 'artifacts'

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    holder_hfid = db.Column(db.Integer)
    site_id = db.Column(db.Integer)
    structure_local_id = db.Column(db.Integer)

    __table_args__ = (db.ForeignKeyConstraint([df_world_id, holder_hfid],
                                 [Historical_Figure.df_world_id,
                                  Historical_Figure.id]), {})

    def __repr__(self):
        return "<Artifact %s>" % (self.name)

class Historical_Event(db.Model):
    __tablename__ = 'historical_events'

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)



'''
class Competitor(db.Model):
    __tablename__ = 'competitors'

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'), 
                            primary_key=True)
    event_id = db.Column(db.Integer, primary_key=True) 
    competitor_hfid = db.Column(db.Integer, primary_key=True)

    __table_args__ = (db.ForeignKeyConstraint(
                         [df_world_id, competitor_hfid],
                         [Historical_Figure.df_world_id,
                         Historical_Figure.id]), {})
'''

class Historical_Era(db.Model):
    __tablename__ = 'historical_eras'

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'),
                            primary_key=True)
    name = db.Column(db.String(50), primary_key=True)
    start_year = db.Column(db.Integer)

    def __repr__(self):
        return "<Historical Era %s>" % (self.name)

