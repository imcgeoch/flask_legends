from . import db


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

    competitions = db.relationship('Competition', 
                          secondary='competitors',
                          backref='competitors', 
                          viewonly=True)
    entity_position_links = db.relationship('Entity_Position_Link',
                                backref='historical_figure',
                                viewonly=True)
    entity_reputations = db.relationship('Entity_Reputation',
                             backref='historical_figure',
                             viewonly=True)

    hf_links = db.relationship('HF_Link', backref='this_histfig',
            foreign_keys='HF_Link.hfid1,HF_Link.df_world_id')
    hf_relationships = db.relationship('Relationship', 
            backref='this_histfig',
            foreign_keys='Relationship.hfid1,Relationship.df_world_id')
    
    site_links = db.relationship('Site_Link', backref='historical_figure', 
                                 viewonly=True)

    skills = db.relationship('Skill')

    interaction_knowledges = db.relationship('Interaction_Knowledge')
    journey_pets = db.relationship('Journey_Pet')
    spheres = db.relationship('Sphere')
    structures = db.relationship('Structure', backref='historical_figures',
                                 viewonly=True)

    def __repr__(self):
        return "<Historical Figure %s>" % (self.name)

class Goal(db.Model):
    __tablename__ = 'goals'
    
    goals = ['create a great work of art', 'immortality', 'master a skill',
             'start a family', 'rule the world', 'fall in love',
             'see the great natural sites', 'become a legendary warrior',
             'bring peace to the world', 'make a great discovery']

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'), 
                            primary_key=True)
    hfid = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.Enum(*goals), primary_key=True)

    __table_args__ = (db.ForeignKeyConstraint([df_world_id, hfid],
                                 [Historical_Figure.df_world_id,
                                  Historical_Figure.id]), {})

class Sphere(db.Model):
    __tablename__ = 'spheres'

    spheres = ['fire', 'wealth', 'caverns', 'misery', 'water', 
               'deformity', 'depravity', 'death', 'thralldom', 
               'chaos', 'blight', 'disease', 'treachery', 'suicide', 
               'nightmares', 'torture', 'animals', 'nature', 
               'plants', 'rivers', 'jewels', 'minerals', 'metals', 
               'mountains', 'fortresses', 'war', 'wisdom', 
               'scholarship', 'writing', 'victory', 'volcanos', 
               'night', 'trickery', 'lies', 'oceans', 'speech', 
               'theft', 'forgiveness', 'mercy', 'creation', 'birth', 
               'youth', 'longevity', 'song', 'truth', 'crafts', 
               'family', 'children', 'murder', 'healing', 
               'lightning', 'dreams', 'rumors', 'fish', 'fishing', 
               'hunting', 'strength', 'light', 'thunder', 'food']
    
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'), 
                            primary_key=True)
    hfid = db.Column(db.Integer, primary_key=True)
    sphere = db.Column(db.Enum(*spheres), primary_key=True)
    
    __table_args__ = (db.ForeignKeyConstraint([df_world_id, hfid],
                                 [Historical_Figure.df_world_id,
                                  Historical_Figure.id]), {})


class Journey_Pet(db.Model):
    __tablename__ = 'journey_pets'
    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer)
    hfid = db.Column(db.Integer)
    journey_pet = db.Column(db.String(20))


    __table_args__ = (db.ForeignKeyConstraint([df_world_id, hfid],
                                 [Historical_Figure.df_world_id,
                                  Historical_Figure.id]), {}) 
class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer)
    hfid = db.Column(db.Integer)
    skill = db.String(20) # should prolly be enum
    total_ip = db.Column(db.Integer)

    __table_args__ = (db.ForeignKeyConstraint([df_world_id, hfid],
                                 [Historical_Figure.df_world_id,
                                  Historical_Figure.id]), {}) 
                                 
class Interaction_Knowledge(db.Model):
    __tablename__ = 'interaction_knowledges'
    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer)
    hfid = db.Column(db.Integer)
    interaction_knowledge = db.Column(db.String(12)) #what is the meaning?
    
    __table_args__ = (db.ForeignKeyConstraint([df_world_id, hfid],
                                 [Historical_Figure.df_world_id,
                                  Historical_Figure.id]), {}) 

class HF_Link(db.Model):
    __tablename__ = 'hf_links'
    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer)
    hfid1 = db.Column(db.Integer)
    hfid2 = db.Column( db.Integer)
    link_strength = db.Column(db.Integer)
    link_type = db.Column(db.Enum('child','spouse'))

    other = db.relationship("Historical_Figure", 
            primaryjoin="and_(HF_Link.hfid2==Historical_Figure.id," + 
                "HF_Link.df_world_id==Historical_Figure.df_world_id)")

    __table_args__ = (db.ForeignKeyConstraint([df_world_id, hfid1],
                                 [Historical_Figure.df_world_id,
                                  Historical_Figure.id]), 
                      db.ForeignKeyConstraint([df_world_id, hfid2],
                                 [Historical_Figure.df_world_id,
                                  Historical_Figure.id]), 
                      {})

class Site_Link(db.Model):
    __tablename__ = 'site_links'

    types = ['lair', 'home structure', 'seat of power', 'occupation']

    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer)
    hfid = db.Column(db.Integer)
    entity_id = db.Column(db.Integer)
    link_type = db.Column(db.Enum(*types))
    occupation_id = db.Column(db.Integer)
    site_id = db.Column(db.Integer)
    sub_id = db.Column(db.Integer)
    
    __table_args__ =( 
        db.ForeignKeyConstraint(['df_world_id', 'hfid'],
                                ['historical_figures.df_world_id',
                                 'historical_figures.id']),
        db.ForeignKeyConstraint(['df_world_id', 'entity_id'],
                                ['entities.df_world_id', 'entities.id']),
        db.ForeignKeyConstraint(['df_world_id', 'site_id'],
                                ['sites.df_world_id', 'sites.id'],
                                ), 
        {})

class Entity_Position_Link(db.Model):
    __tablename__ = 'entity_position_links'
    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer)
    hfid = db.Column(db.Integer)
    entity_id = db.Column(db.Integer)
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    position_profile_id = db.Column(db.Integer)
  
    __table_args__ = (
        db.ForeignKeyConstraint(['df_world_id', 'hfid'],
                                ['historical_figures.df_world_id',
                                 'historical_figures.id']),
        db.ForeignKeyConstraint(['df_world_id', 'entity_id'],
                                ['entities.df_world_id', 'entities.id']),
        {})

class Entity_Reputation(db.Model):
    __tablename__ = 'entity_reputations'
    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer)
    hfid = db.Column(db.Integer)
    entity_id = db.Column(db.Integer)
    first_ageless_season_count = db.Column(db.Integer)
    first_ageless_year = db.Column(db.Integer)
    unsolved_murders = db.Column(db.Integer)
  
    __table_args__ = (
        db.ForeignKeyConstraint(['df_world_id', 'hfid'],
                                ['historical_figures.df_world_id',
                                 'historical_figures.id']),
        db.ForeignKeyConstraint(['df_world_id', 'entity_id'],
                                ['entities.df_world_id', 'entities.id']),
        {})

class Relationship(db.Model):
    __tablename__ = 'relationship'
    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer)
    hfid1 = db.Column(db.Integer)
    hfid2 = db.Column(db.Integer)
    known_identity_id = db.Column(db.Integer)
    last_meet_seconds72 = db.Column(db.Integer)
    last_meet_year = db.Column(db.Integer)
    meet_count = db.Column(db.Integer)
    rep = db.Column(db.Integer) # only one of buddy, info source ever used

    other = db.relationship("Historical_Figure", primaryjoin=
    "and_(Relationship.hfid2==Historical_Figure.id," + 
    "Relationship.df_world_id==Historical_Figure.df_world_id)")

    __table_args__ = (db.ForeignKeyConstraint([df_world_id, hfid1],
                                 [Historical_Figure.df_world_id,
                                  Historical_Figure.id]), 
                      db.ForeignKeyConstraint([df_world_id, hfid2],
                                 [Historical_Figure.df_world_id,
                                  Historical_Figure.id]), 
                      {})


