from . import db
from .join_builder import join_builder as jb, table_join_builder as tjb


class Historical_Figure(db.Model):
    __tablename__ = 'historical_figures'

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'),
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    race = db.Column(db.String(40))
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
                                     foreign_keys='Artifact.holder_hfid,'
                                                  'Artifact.df_world_id',
                                     primaryjoin=jb('Historical_Figure',
                                                    'Artifact',
                                                    ('id', 'holder_hfid')),
                                     viewonly=True)

    competitions = db.relationship('Competition', 
                          secondary='competitors',
                          backref='competitors', 
                          primaryjoin=tjb('Historical_Figure',
                                          'competitors',
                                          ('id', 'competitor_hfid')),
                          secondaryjoin=tjb('Historical_Event',
                                            'competitors',
                                            ('id', 'event_id')),
                          viewonly=True)
    entity_position_links = db.relationship('Entity_Position_Link',
                                backref='historical_figure',
                                viewonly=True, foreign_keys=[id, df_world_id],
                                primaryjoin=jb('Historical_Figure', 
                                               'Entity_Position_Link',
                                               ('id', 'hfid')))
    entity_reputations = db.relationship('Entity_Reputation',
                             backref='historical_figure',
                             viewonly=True, foreign_keys=[id, df_world_id],
                             primaryjoin=jb('Historical_Figure', 
                                            'Entity_Reputation',
                                               ('id', 'hfid')))
    entity_links =  db.relationship('Entity_Link',
                             backref='historical_figure',
                             viewonly=True, foreign_keys=[id, df_world_id],
                             primaryjoin=jb('Historical_Figure', 
                                            'Entity_Link',
                                               ('id', 'hfid')))
    written_contents = db.relationship('Written_Content',
                                       backref='author',
                                       viewonly=True, 
                                       foreign_keys="Written_Content.df_world_id,"
                                                    "Written_Content.author_hfid",
                                       primaryjoin=jb('Historical_Figure',
                                                      'Written_Content',
                                                      ('id', 'author_hfid')))

    hf_links = db.relationship('HF_Link', backref='this_histfig',
            foreign_keys='HF_Link.hfid1,HF_Link.df_world_id',
            viewonly=True,
            primaryjoin=jb('Historical_Figure', 'HF_Link', ('id', 'hfid1')))
    hf_relationships = db.relationship('Relationship', 
            backref='this_histfig', primaryjoin=jb('Historical_Figure', 
                                                    'Relationship', ('id', 'hfid1')),
            foreign_keys='Relationship.hfid1,Relationship.df_world_id')
    
    site_links = db.relationship('Site_Link', backref='historical_figure', 
                                 viewonly=True, foreign_keys = [id, df_world_id],
                                 primaryjoin=jb('Historical_Figure', 'Site_Link', 
                                                ('id', 'hfid')))
    skills = db.relationship('Skill', viewonly=True, 
                            foreign_keys="Skill.hfid,Skill.df_world_id",
                            primaryjoin=jb("Historical_Figure", 
                                           "Skill", ("id", "hfid")))

    interaction_knowledges = db.relationship('Interaction_Knowledge', 
                                 viewonly=True, 
                                 foreign_keys="Interaction_Knowledge.hfid,"
                                              "Interaction_Knowledge.df_world_id",
                                 primaryjoin=jb("Historical_Figure", 
                                                "Interaction_Knowledge", 
                                                ("id", "hfid")))
    journey_pets = db.relationship('Journey_Pet', viewonly=True, 
                            foreign_keys="Journey_Pet.hfid,Journey_Pet.df_world_id",
                            primaryjoin=jb("Historical_Figure", 
                                           "Journey_Pet", ("id", "hfid")))
    spheres = db.relationship('Sphere', viewonly=True, 
                            foreign_keys="Sphere.hfid,Sphere.df_world_id",
                            primaryjoin=jb("Historical_Figure", 
                                           "Sphere", ("id", "hfid")))
    goals = db.relationship('Goal', viewonly=True, 
                            foreign_keys="Goal.hfid,Goal.df_world_id",
                            primaryjoin=jb("Historical_Figure", 
                                           "Goal", ("id", "hfid")))
    structures = db.relationship('Structure', backref='historical_figures',
                                 viewonly=True, foreign_keys=[id, df_world_id],
                                 primaryjoin=jb('Historical_Figure', 'Structure',
                                                ('id', 'worship_hfid')))

    def first_name(self):
        return self.name.split(" ")[0] 

    prim_events = db.relationship('Historical_Event', backref='hf', 
                    primaryjoin='and_(Historical_Event.hfid == ' +
                                        'Historical_Figure.id,' +
                                      'Historical_Event.df_world_id == ' +
                                         'Historical_Figure.df_world_id)',
                    foreign_keys=[id, df_world_id], uselist=True)

    sec_events = db.relationship('Historical_Event', backref='hf2', 
                    primaryjoin='and_(Historical_Event.hfid2 == ' +
                                        'Historical_Figure.id,' +
                                      'Historical_Event.df_world_id == ' +
                                         'Historical_Figure.df_world_id)',
                    foreign_keys=[id, df_world_id], uselist=True)
    
    all_events = db.relationship('Historical_Event', 
                    primaryjoin='and_(' +
                                   'or_(Historical_Event.hfid == ' +
                                        'Historical_Figure.id,' +
                                   'Historical_Event.hfid2 == ' +
                                        'Historical_Figure.id),' +
                                      'Historical_Event.df_world_id == ' +
                                         'Historical_Figure.df_world_id)',
                    foreign_keys=[id, df_world_id], uselist=True)


    def __repr__(self):
        return "<Historical Figure %s>" % (self.name)

class Goal(db.Model):
    __tablename__ = 'goals'
    
    goals = ['create a great work of art', 'immortality', 'master a skill',
             'start a family', 'rule the world', 'fall in love',
             'see the great natural sites', 'become a legendary warrior',
             'bring peace to the world', 'make a great discovery',
             'craft a masterwork']

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'), 
                            primary_key=True)
    hfid = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.Enum(*goals, name='goal_types'), primary_key=True)

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
               'hunting', 'strength', 'light', 'thunder', 'food', 
               'rebirth', 'muck', 'art', 'inspiration', 'sky', 'wind']
    
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'), 
                            primary_key=True)
    hfid = db.Column(db.Integer, primary_key=True)
    sphere = db.Column(db.String(20), primary_key=True)

class Journey_Pet(db.Model):
    __tablename__ = 'journey_pets'
    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'))
    hfid = db.Column(db.Integer)
    journey_pet = db.Column(db.String(40))

class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'))
    hfid = db.Column(db.Integer)
    skill = db.Column(db.String(40)) # should prolly be enum
    total_ip = db.Column(db.Integer)

class Interaction_Knowledge(db.Model):
    __tablename__ = 'interaction_knowledges'
    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'))
    hfid = db.Column(db.Integer)
    interaction_knowledge = db.Column(db.String(12)) #what is the meaning?

class Entity_Link(db.Model):
    __tablename__ = 'entity_links'
    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'))
    hfid = db.Column(db.Integer)
    entity_id = db.Column(db.Integer)
    link_type = db.Column(db.String(20))

class HF_Link(db.Model):
    __tablename__ = 'hf_links'
    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'))
    hfid1 = db.Column(db.Integer)
    hfid2 = db.Column( db.Integer)
    link_strength = db.Column(db.Integer)
    link_type = db.Column(db.Enum('child','spouse', 'deity', 'apprentice',
        'mother', 'father', 'former apprentice', 'master', 'prisoner', 'imprisoner',
        'former master', name='hf_link_type'))

    other = db.relationship("Historical_Figure", foreign_keys=[df_world_id, hfid2],
            primaryjoin="and_(HF_Link.hfid2==Historical_Figure.id," + 
                "HF_Link.df_world_id==Historical_Figure.df_world_id)")

class Site_Link(db.Model):
    __tablename__ = 'site_links'

    types = ['lair', 'home structure', 'seat of power', 'occupation', 'hangout']

    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'))
    hfid = db.Column(db.Integer)
    entity_id = db.Column(db.Integer)
    link_type = db.Column(db.Enum(*types, name='site_link_types'))
    occupation_id = db.Column(db.Integer)
    site_id = db.Column(db.Integer)
    sub_id = db.Column(db.Integer)
   
class Entity_Position_Link(db.Model):
    __tablename__ = 'entity_position_links'
    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'))
    hfid = db.Column(db.Integer)
    entity_id = db.Column(db.Integer)
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    position_profile_id = db.Column(db.Integer)


class Entity_Reputation(db.Model):
    __tablename__ = 'entity_reputations'
    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'))
    hfid = db.Column(db.Integer)
    entity_id = db.Column(db.Integer)
    first_ageless_season_count = db.Column(db.Integer)
    first_ageless_year = db.Column(db.Integer)
    unsolved_murders = db.Column(db.Integer)
  

class Relationship(db.Model):
    __tablename__ = 'relationship'
    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'))
    hfid1 = db.Column(db.Integer)
    hfid2 = db.Column(db.Integer)
    known_identity_id = db.Column(db.Integer)
    last_meet_seconds72 = db.Column(db.Integer)
    last_meet_year = db.Column(db.Integer)
    meet_count = db.Column(db.Integer)
    rep_buddy = db.Column(db.Integer) 

    other = db.relationship("Historical_Figure", foreign_keys=[df_world_id, hfid2],
            primaryjoin=
    "and_(Relationship.hfid2==Historical_Figure.id," + 
    "Relationship.df_world_id==Historical_Figure.df_world_id)")
