from . import db
from .join_builder import join_builder as jb, table_join_builder as tjb


class Historical_Figure(db.Model):
    __tablename__ = 'historical_figures'

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', 
                            ondelete='CASCADE'), primary_key=True)
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

    
    first_name = lambda self: self.name.split(" ")[0]
    pronouns = lambda self: ('he', 'his') if self.caste == 'MALE' else ('she', 'her') 

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
                                viewonly=True, #foreign_keys=[id, df_world_id],
                                foreign_keys="Entity_Position_Link.df_world_id,"
                                             "Entity_Position_Link.hfid",
                                primaryjoin=jb('Historical_Figure', 
                                               'Entity_Position_Link',
                                               ('id', 'hfid')))
    entity_reputations = db.relationship('Entity_Reputation',
                             backref='historical_figure',
                             viewonly=True, #foreign_keys=[id, df_world_id],
                             foreign_keys="Entity_Reputation.df_world_id,"
                                          "Entity_Reputation.hfid",
                             primaryjoin=jb('Historical_Figure', 
                                            'Entity_Reputation',
                                               ('id', 'hfid')))
    entity_links =  db.relationship('Entity_Link',
                             backref='historical_figure',
                             viewonly=True, #foreign_keys=[id, df_world_id],
                             foreign_keys="Entity_Link.df_world_id,"
                                          "Entity_Link.hfid",
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
    hf_relationships_historical = db.relationship('Relationship_Historical', 
            backref='this_histfig', primaryjoin=jb('Historical_Figure', 
                                                'Relationship_Historical', ('id', 'hfid1')),
            foreign_keys='Relationship_Historical.hfid1,Relationship_Historical.df_world_id')
    vague_relationships = db.relationship('Vague_Relationship', 
            backref='this_histfig', primaryjoin=jb('Historical_Figure', 
                                                'Vague_Relationship', ('id', 'hfid1')),
            foreign_keys='Vague_Relationship.hfid1,Vague_Relationship.df_world_id')

    site_links = db.relationship('Site_Link', backref='historical_figure', 
                                 viewonly=True, #foreign_keys = [id, df_world_id],
                                 foreign_keys="Site_Link.df_world_id,"
                                              "Site_Link.hfid",
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
    temples = db.relationship('Structure', backref='historical_figure',
                                 viewonly=True, #foreign_keys=[id, df_world_id],
                                 foreign_keys="Structure.df_world_id,"
                                              "Structure.df_world_id",
                                 primaryjoin=jb('Historical_Figure', 'Structure',
                                                ('id', 'worship_hfid')))
    
    positions = db.relationship("Entity_Position_Assignment",
            backref='hf', viewonly=True,
            foreign_keys="Entity_Position_Assignment.df_world_id,"
                         "Entity_Position_Assignment.histfig",
            primaryjoin=jb("Historical_Figure", "Entity_Position_Assignment",
                           ('id', 'histfig')))


    prim_events = db.relationship('Historical_Event', backref='hf', 
                    primaryjoin='and_(Historical_Event.hfid == ' +
                                        'Historical_Figure.id,' +
                                      'Historical_Event.df_world_id == ' +
                                         'Historical_Figure.df_world_id)',
                    foreign_keys="Historical_Event.df_world_id,"
                                 "Historical_Event.hfid")

    sec_events = db.relationship('Historical_Event', backref='hf2', 
                    primaryjoin='and_(Historical_Event.hfid2 == ' +
                                        'Historical_Figure.id,' +
                                      'Historical_Event.df_world_id == ' +
                                         'Historical_Figure.df_world_id)',
                    foreign_keys="Historical_Event.df_world_id,"
                                 "Historical_Event.hfid2")
    
    all_events = db.relationship('Historical_Event', 
                    primaryjoin='and_(' +
                                   'or_(Historical_Event.hfid == ' +
                                        'Historical_Figure.id,' +
                                   'Historical_Event.hfid2 == ' +
                                        'Historical_Figure.id),' +
                                      'Historical_Event.df_world_id == ' +
                                         'Historical_Figure.df_world_id)',
                    foreign_keys="Historical_Event.df_world_id,"
                                 "Historical_Event.hfid,"
                                 "Historical_Event.hfid2",
                    order_by="Historical_Event.year,Historical_Event.seconds72")
    
    intrigue_actors = db.relationship('Intrigue_Actor',
            backref='parent_hf', viewonly=True,
            foreign_keys="Intrigue_Actor.df_world_id, Intrigue_Actor.parent_hfid",
            primaryjoin=jb("Historical_Figure", "Intrigue_Actor", ("id", "parent_hfid")))
    intrigue_plots = db.relationship('Intrigue_Plot',
            backref='parent_hf', viewonly=True,
            foreign_keys="Intrigue_Plot.df_world_id, Intrigue_Plot.hfid",
            primaryjoin=jb("Historical_Figure", "Intrigue_Plot", ("id", "hfid")))


    def __repr__(self):
        return "<Historical Figure %s>" % (self.name)

class Goal(db.Model):
    __tablename__ = 'goals'
    
    goals = ['create a great work of art', 'immortality', 'master a skill',
             'start a family', 'rule the world', 'fall in love',
             'see the great natural sites', 'become a legendary warrior',
             'bring peace to the world', 'make a great discovery',
             'craft a masterwork', 'attain rank in society', 'bathe world in chaos']

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
        'former master', 'former spouse', 'deceased spouse', 'lover', name='hf_link_type'))

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
    love = db.Column(db.Integer)
    respect = db.Column(db.Integer)
    trust = db.Column(db.Integer)
    loyalty = db.Column(db.Integer)
    fear = db.Column(db.Integer)

    other = db.relationship("Historical_Figure", foreign_keys=[df_world_id, hfid2],
            primaryjoin=
    "and_(Relationship.hfid2==Historical_Figure.id," + 
    "Relationship.df_world_id==Historical_Figure.df_world_id)")

class Relationship_Historical(db.Model):
    __tablename__ = 'relationship_historical'
    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'))
    hfid1 = db.Column(db.Integer)
    hfid2 = db.Column(db.Integer)
    love = db.Column(db.Integer)
    respect = db.Column(db.Integer)
    trust = db.Column(db.Integer)
    loyalty = db.Column(db.Integer)
    fear = db.Column(db.Integer)

    other = db.relationship("Historical_Figure", foreign_keys=[df_world_id, hfid2],
            primaryjoin=
    "and_(Relationship_Historical.hfid2==Historical_Figure.id," + 
    "Relationship_Historical.df_world_id==Historical_Figure.df_world_id)")

class Vague_Relationship(db.Model):
    __tablename__ = 'vague_relationship'
    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'))
    hfid1 = db.Column(db.Integer)
    hfid2 = db.Column(db.Integer)
    war_buddy = db.Column(db.Boolean)
    athlete_buddy = db.Column(db.Boolean)
    athletic_rival = db.Column(db.Boolean)
    childhood_friend = db.Column(db.Boolean)
    jealous_obsession = db.Column(db.Boolean)

    other = db.relationship("Historical_Figure", foreign_keys=[df_world_id, hfid2],
            primaryjoin=
    "and_(Vague_Relationship.hfid2==Historical_Figure.id," + 
    "Vague_Relationship.df_world_id==Historical_Figure.df_world_id)")

class Identity(db.Model):
    __tablename__ = 'identities'
    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'), primary_key=True)
    name = db.Column(db.String(100))
    race = db.Column(db.String(40))
    caste = db.Column(db.String(10))
    birth_seconds72 = db.Column(db.Integer) 
    birth_year = db.Column(db.Integer)
    profession = db.Column(db.String(50))
    entity_id = db.Column(db.Integer)
    histfig_id = db.Column(db.Integer) # seems to be redundant with histfig.used_identity_id
    nemisis_id = db.Column(db.Integer)

    true_identity = db.relationship("Historical_Figure", backref="false_identity",
            foreign_keys="Historical_Figure.df_world_id,"
                         "Historical_Figure.id",
            primaryjoin=jb("Identity","Historical_Figure",("histfig_id", "id")),
            viewonly=True)

class Intrigue_Actor(db.Model):
    __tablename__ = 'intrigue_actors'
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'),
            primary_key=True)
    parent_hfid = db.Column(db.Integer, primary_key=True)
    local_id = db.Column(db.Integer, primary_key=True)

    hfid = db.Column(db.Integer)
    role = db.Column(db.String(30))
    strategy = db.Column(db.String(30))

    target = db.relationship("Historical_Figure", backref="intrigue_actors_on",
            foreign_keys="Historical_Figure.df_world_id,"
                         "Historical_Figure.id",
            primaryjoin=jb("Intrigue_Actor","Historical_Figure",("hfid", "id")),
            viewonly=True)

class Intrigue_Plot(db.Model):
    __tablename__ = 'intrigue_plots'
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'),
            primary_key=True)
    hfid = db.Column(db.Integer, primary_key=True)
    local_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    on_hold = db.Column(db.Boolean)
    entity_id = db.Column(db.Integer)

    

