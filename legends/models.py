import enum

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

class Artifact(db.Model):
    __tablename__ = 'artifacts'

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    name_string = db.Column(db.String(50))
    page_number = db.Column(db.Integer)
    # page_written_content_id = db.Column(db.Integer) redundant scroll vs book
    written_content_id = db.Column(db.Integer)
    holder_hfid = db.Column(db.Integer)
    site_id = db.Column(db.Integer)
    structure_local_id = db.Column(db.Integer)

    __table_args__ = (db.ForeignKeyConstraint([df_world_id, holder_hfid],
                                 [Historical_Figure.df_world_id,
                                  Historical_Figure.id]), {})

    # add lookup to written_contents

    def __repr__(self):
        return "<Artifact %s>" % (self.name)



class Historical_Era(db.Model):
    __tablename__ = 'historical_eras'

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'),
                            primary_key=True)
    name = db.Column(db.String(50), primary_key=True)
    start_year = db.Column(db.Integer)

    def __repr__(self):
        return "<Historical Era %s>" % (self.name)

class Region(db.Model):
    __tablename__ = 'regions'

    types = ['Wetland', 'Grassland', 'Hills', 'Desert', 'Forest',
             'Mountains', 'Lake', 'Ocean', 'Tundra', 'Glacier']

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    type = db.Column(db.Enum(*types))

class Underground_Region(db.Model):
    __tablename__ = 'underground_regions'

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum('cavern', 'magma', 'underworld'))


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

    site_links = db.relationship('Site_Link', backref='site', viewonly=True)
    structures = db.relationship('Structure', backref='site', viewonly=True)

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
    type = db.Column(db.Enum(*types))
    subtype = db.Column(db.Enum(*subtypes))
    worship_hfid = db.Column(db.Integer)

    __table_args__ = (db.ForeignKeyConstraint([df_world_id, site_id],
                                 [Site.df_world_id, Site.id]),
                      db.ForeignKeyConstraint([df_world_id, entity_id],
                                 [Entity.df_world_id, Entity.id]),
                      db.ForeignKeyConstraint([df_world_id, worship_hfid],
                                 [Historical_Figure.df_world_id,
                                  Historical_Figure.id]), {})

class World_Construction(db.Model):
    __tablename__ = 'world_constructions'
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    type = db.Column(db.String(50)) #should be enum
    coords = db.Column(db.String(50))

class Written_Content(db.Model):
    __tablename__ = 'written_contents'
    
    forms = ['musical composition', 'choreography', 'pom', 'guide',
             'essay', 'manual', 'cultural history', 'star chart', 
             'letter', 'short story', 'cultural composition', 'novel', 
             'autobiography', 'comparative biography', 'biography']

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    form = db.Column(db.Enum(*forms))
    form_id = db.Column(db.Integer) # use primaryjoin with form_id == TYPE 
    author_hfid = db.Column(db.Integer)
    author_roll = db.Column(db.Integer)

    styles = db.relationship('Style')
    
    __table_args__ = (db.ForeignKeyConstraint([df_world_id, author_hfid],
                                 [Historical_Figure.df_world_id,
                                  Historical_Figure.id]), {})

class Style(db.Model):
    __tablename__ = 'styles'

    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer)
    content_id = db.Column(db.Integer)
    style = db.Column(db.String(10)) #should be enum
    magnitude = db.Column(db.Integer)
    __table_args__ = (db.ForeignKeyConstraint([df_world_id, content_id],
                                 [Written_Content.df_world_id,
                                  Written_Content.id]), {})

class Musical_Form(db.Model):
    __tablename__ = 'musical_forms'
    
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text())

class Poetic_Form(db.Model):
    __tablename__ = 'poetic_forms'
    
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text())

### BEGIN HISTORICAL EVENTS

class Historical_Event(db.Model):
    __tablename__ = 'historical_events'

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    year = db.Column(db.Integer)
    seconds72 = db.Column(db.Integer)

    # shared columns
    hfid = db.Column(db.Integer)
    hfid2 = db.Column(db.Integer)
    entity_id = db.Column(db.Integer)
    entity_id2 = db.Column(db.Integer)
    artifact_id = db.Column(db.Integer)
    site_id = db.Column(db.Integer)
    unit_id = db.Column(db.Integer)
  
    link_type = db.Column(db.String(20))
    
    __mapper_args__ = {
        'polymorphic_identity':'historical_event',
        'polymorphic_on':'type'
    }


'''
class Change_HF_State_Event(Historical_Event):
    #hfid = db.Column(db.Integer)
    state = db.Column(db.String(20))
    coords = db.Column(db.String(20))
    feature_layer_id = db.Column(db.Integer)
    site_id = db.Column(db.Integer)
    subregion_id = db.Column(db.Integer)

    __mapper_args__ = { 'polymorphic_identity':'change_hf_state'}
'''

class Add_HF_Entity_Link(Historical_Event):
    # entity_id = db.Column(db.Integer)
    # to be calc'd
    # link_type = db.Column(db.String(20))
    # hfid = db.Column(db.Integer) 
    position = db.Column(db.String(20))
    
    __mapper_args__ = { 'polymorphic_identity':'add_hf_entity_link'}

class Add_HF_HF_Link(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'add_hf_hf_link'}

    #hfid = db.Column(db.Integer)
    #hfid_target = db.Column(db.Integer) # hfid2

    # to be calc'd 
    # link_type = db.Column(db.String(20))

class Add_HF_Site_Link(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'add_hf_site_link'}

    # site_id = db.Column(db.Integer)
    # to be calc'd
    # link_type = db.Column(db.String(20))
    # hfid = db.Column(db.Integer)
    # entity_id = db.Column(db.Integer)
    building = db.Column(db.Integer)

class Agreement_Formed(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'agreement_formed'}

    agreement_id = db.Column(db.Integer)
    #hfid = db.Column(db.Integer)
    #site_id = db.Column(db.Integer)
    #artifact_id = db.Column(db.Integer)

    #concluder_hfid, subject_id, reason in java but not seen in xml


class Artifact_Claim_Formed(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact_claim_formed'}

    #hfid = db.Column(db.Integer)
    #artifact_id = db.Column(db.Integer)
    #entity_id = db.Column(db.Integer)
    position_profile_id = db.Column(db.Integer)
    claim = db.Column(db.Enum('heirloom', 'symbol', 'treasure'))

class Artifact_Copied(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact_copied'}

    # artifact_id = db.Column(db.Integer)
    dest_site_id = db.Column(db.Integer)
    dest_structure_id = db.Column(db.Integer)
    dest_entity_id = db.Column(db.Integer)
    source_site_id = db.Column(db.Integer)
    source_structure_id = db.Column(db.Integer)
    source_entity_id = db.Column(db.Integer)
    from_original = db.Column(db.Boolean)

class Artifact_Created(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact_created'}

    #artifact_id = db.Column(db.Integer)
    #hfid = db.Column(db.Integer)
    # unit_id = db.Column(db.Integer)
    #site_id = db.Column(db.Integer)

class Artifact_Destroyed(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact_destroyed'}

    #artifact_id = db.Column(db.Integer)
    #site_id = db.Column(db.Integer)
    #entity_id = db.Column(db.Integer)

class Artifact_Found(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact_found'}

    #artifact_id = db.Column(db.Integer)
    #hfid = db.Column(db.Integer)
    # unit_id = db.Column(db.Integer)
    #site_id = db.Column(db.Integer)


class Artifact_Given(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact_given'}

    #artifact_id = db.Column(db.Integer)
    #giver_hfid = db.Column(db.Integer)
    #giver_entity_id = db.Column(db.Integer)
    #receiver_hfid = db.Column(db.Integer) hfid2
    #receiver_entity_id = db.Column(db.Integer)
    reason = db.Column(db.String(20))

class Artifact_Lost(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact_lost'}
