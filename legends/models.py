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
    # lookups
    hfid = db.Column(db.Integer)
    hfid2 = db.Column(db.Integer)
    entity_id = db.Column(db.Integer)
    entity_id2 = db.Column(db.Integer)
    artifact_id = db.Column(db.Integer)
    site_id = db.Column(db.Integer)
    unit_id = db.Column(db.Integer)
    site_civ_id = db.Column(db.Integer) # local group?
    new_site_civ_id = db.Column(db.Integer)
    reason_id = db.Column(db.Integer)
    circumstance_id = db.Column(db.Integer)
    wcid = db.Column(db.Integer)
    
    ## item fields
    item = db.Column(db.Integer)
    mat = db.Column(db.String(20))
    item_type = db.Column(db.String(20))
    item_subtype = db.Column(db.String(20))
    mat_type = db.Column(db.Integer)
    mat_index = db.Column(db.Integer)
    dye_mat_type = db.Column(db.Integer)
    ####
  
    # strings
    link_type = db.Column(db.String(20))
    reason = db.Column(db.String(50))
    position = db.Column(db.String(20))
    interaction = db.Column(db.String(50))
    action = db.Column(db.Integer)
    circumstance = db.Column(db.String(50))
    topic = db.Column(db.String(30))
    first = db.Column(db.Boolean)
    
    __mapper_args__ = {
        'polymorphic_identity':'historical_event',
        'polymorphic_on':'type'
    }

class Add_HF_Entity_Link(Historical_Event):
    # entity_id = db.Column(db.Integer)
    # to be calc'd or not?
    # link_type = db.Column(db.String(20))
    # hfid = db.Column(db.Integer) 
    #position = db.Column(db.String(20))
    
    __mapper_args__ = { 'polymorphic_identity':'add hf entity link'}

class Add_HF_HF_Link(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'add hf hf link'}

    #hfid = db.Column(db.Integer)
    #hfid_target = db.Column(db.Integer) # hfid2

    # to be calc'd or_not
    # link_type = db.Column(db.String(20))

class Add_HF_Site_Link(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'add hf site link'}

    # site_id = db.Column(db.Integer)
    # to be calc'd or not?
    # link_type = db.Column(db.String(20))
    # hfid = db.Column(db.Integer)
    # entity_id = db.Column(db.Integer)
    building = db.Column(db.Integer)

class Agreement_Formed(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'agreement formed'}

    agreement_id = db.Column(db.Integer)
    #hfid = db.Column(db.Integer)
    #site_id = db.Column(db.Integer)
    #artifact_id = db.Column(db.Integer)

    #concluder_hfid, subject_id, reason in java but not seen in xml


class Artifact_Claim_Formed(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact claim formed'}

    #hfid = db.Column(db.Integer)
    #artifact_id = db.Column(db.Integer)
    #entity_id = db.Column(db.Integer)
    position_profile_id = db.Column(db.Integer)
    claim = db.Column(db.Enum('heirloom', 'symbol', 'treasure'))

class Artifact_Copied(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact copied'}

    # artifact_id = db.Column(db.Integer)
    dest_site_id = db.Column(db.Integer)
    dest_structure_id = db.Column(db.Integer)
    dest_entity_id = db.Column(db.Integer)
    source_site_id = db.Column(db.Integer)
    source_structure_id = db.Column(db.Integer)
    source_entity_id = db.Column(db.Integer)
    from_original = db.Column(db.Boolean)

class Artifact_Created(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact created'}

    #artifact_id = db.Column(db.Integer)
    #hfid = db.Column(db.Integer)
    # unit_id = db.Column(db.Integer)
    #site_id = db.Column(db.Integer)

class Artifact_Destroyed(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact destroyed'}

    #artifact_id = db.Column(db.Integer)
    #site_id = db.Column(db.Integer)
    #entity_id = db.Column(db.Integer)

class Artifact_Found(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact found'}

    #artifact_id = db.Column(db.Integer)
    #hfid = db.Column(db.Integer)
    # unit_id = db.Column(db.Integer)
    #site_id = db.Column(db.Integer)


class Artifact_Given(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact given'}

    #artifact_id = db.Column(db.Integer)
    #giver_hfid = db.Column(db.Integer)
    #giver_entity_id = db.Column(db.Integer)
    #receiver_hfid = db.Column(db.Integer) hfid2
    #receiver_entity_id = db.Column(db.Integer)
    #reason = db.Column(db.String(50))

class Artifact_Lost(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact lost'}

    #artifact_id
    #site_id

class Artifact_Posessed(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact posessed'}
    # hfid
    # artifact_id
    # unit_id
    # site_id

    #reason = db.Column(db.String(50))
    #reason_id = db.Column(db.Integer)
    # circumstance = db.Column(db.String(50))
    #circumstance_id = db.Column(db.Integer)


class Artifact_Recovered(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact recovered'}

    # hfid
    # artifact_id
    # unit_id
    # site_id

class Artifact_Stored(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'artifact stored'}
    
    # hfid
    # artifact_id
    # unit_id
    # site_id

class Artifact_Transformed(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'artifact transformed'}
    new_artifact_id = db.Column(db.Integer)
    # artifact_id
    # unit_id
    # site_id
    # hfid

class Assume_Identity(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'assume identity'}

    #hfid
    identity_id = db.Column(db.Integer)
    #entity_id

class Attacked_Site(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'attacked site'}

    #hfid attacker_general
    #hfid2 defender_general
    #entity_id attacker_civ_id
    #entity_id2 defender_civ_id
    #siteid
    #site_civ_id = db.Column(db.Integer)

class Body_Abused(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'body abused'}
    # hfid
    # entity_id
    abuse_type = db.Column(db.Integer)
    #site 

class Change_HF_Body_State(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'change hf body state'}
    #hfid
    body_state = db.Column(db.String(20))
    #siteid
    building_id = db.Column(db.Integer)

class Change_HF_Job(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'change hf job'}
    old_job = db.Column(db.String(20))
    new_job = db.Column(db.String(20))
    #hfid

class Change_HF_State(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'change hf state'}
    subregion_id = db.Column(db.Integer)
    #hfid = db.Column(db.Integer)
    state = db.Column(db.String(20))

class Change_Creature_Type(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'change creature type'}
    #hfid1 changer
    #hfid2 changee
    old_race = db.Column(db.String(20))
    new_race = db.Column(db.String(20))
    old_caste = db.Column(db.String(20))
    new_caste = db.Column(db.String(20))


class Create_Entity_Position(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'create entity position'}
    #hfid
    #entity_id civ
    #site_civ_id = db.Column(db.Integer)
    #reason
    # position = db.Column(db.String(20))

class Created_Site(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'created site'}

    #hfid builder_hfid
    #site_id
    #entity_id civid
    #site_civ_id sitecivid

class Created_Strucure(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'created structure'}
    
    #hfid builder_hfid
    #site_id
    #entity_id civid
    #site_civ_id sitecivid
    #structure_id 

class Created_World_Construction(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'created world construction'}

    #site
    #site_civ
    # wcid = db.Column(db.Integer)
    master_wcid = db.Column(db.Integer)
    site_id2 = db.Column(db.Integer)

class Creature_Devoured(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'creature devoured'}

    # hfid1 victim 
    # hfid2 eater 
    # entity
    # site

    race = db.Column(db.String(20))
    caste = db.Column(db.String(20))
   
class Destroyed_Site(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'destroyed site'}

    #attacker = db.synonym('entity_id')
    #defender = db.synonym('entity_id2')
    #site
    #site_civ

class Diplomat_Lost(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'diplomat lost'}

    #entity 
    # entity2 involved
    #site

class Entity_Created(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'entity created'}
    #entity_id
    #siteid
    #structureid

class Entity_Law(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'entity law'}
    #hfid
    #entity id
    law_type = db.Column(db.Enum('add', 'remove')) #add or remove
    law = db.Column(db.String(50))

class Entity_Primary_Criminals(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'entity primary criminals'}
    # enid
    # siteid
    # structureid
    # action = db.Column(db.Integer)

class Entity_Searched_Site(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'entity searched site'}
    # edid (searcher civ)
    # siteid
    result = db.Column(db.String(20))

class Field_Battle(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'field battle'}
    # hfid
    # hfid2
    #entityid
    #entityid2
    # location

class Field_Contact(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'field contact'}
    #enid1
    #enid2
    #siteid

class HF_Abducted(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf abducted'}
    # hfid
    # hfid2
    # location

class HF_Attacked_Site(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf attacked site'}

    # hfid 
    # entity_id
    # site_civ_id
    # site_id

class HF_Confronted(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf confronted'}
    # hfid
    situation = db.Column(db.String(50))
    # reason = db.Column(db.String(50))
    # location

class HF_Destroyed_Site(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf destroyed site'}
    # hfid1
    # entity_id
    # site_civ_id
    # site_id

class HF_Died(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf died'}

    # hfid
    # hfid2 slayer
    # artifact_id ?
    # location
    slayer_race = db.Column(db.String(20))
    slayer_caste = db.Column(db.String(20))
    slayer_item_id = db.Column(db.Integer)
    slayer_shooter_item_id = db.Column(db.Integer)
    cause = db.Column(db.String(20))

class HF_Does_Interaction(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf does interaction'}

    #hfid doer_hfid
    #hfid target_hfid
    #location
    #interaction = db.Column(db.String(50))
    interaction_action = db.Column(db.String(20))
    interaction_string = db.Column(db.String(20))
    source = db.Column(db.Integer)
class HF_Gains_Secret_Goal(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf gains secret goal'}

    #hfid
    secret_goal = db.Column(db.String(20))

class HF_Learns_Secret(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf learns secret'}

    #hifd studet
    #hfid teacher
    #artifact_id
    #interaction = db.Column(db.String(50))
    secret_text = db.Column(db.String(50))

class HF_New_Pet(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf new pet'}
    # hfid group/grouphfid
    pets = db.Column(db.String(50))
    # location

class HF_Prayed_Inside_Structure(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf prayed inside structure'}
    #hf
    #site
    #structure

class HF_Profaned_Structure(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf profaned structure'}
    #hf
    #site
    #structure
    # action = db.Column(db.Integer)

class HF_Reach_Summit(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf reach summit'}
    #location
    #relationship with hf (multiple possible?)

class HF_Recruited_Unit_Type_For_Entity(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':
                            'hf recruited unit type for entity'}
    #hfid
    #entityid
    #siteid
    unit_type = db.Column(db.String(20))

class HF_Relationship_Denied(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf relationship denied'}

    #hdif seeker_hfid
    #hfid2 target_hfid
    relationship = db.Column(db.String(20))
    #reason
    #reason_id = db.Column(db.Integer)

class HF_Reunion(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf reunion'}

    #hfid group1hfid
    #relationship with hfid (multiple targetsi possible)

class HF_Revived(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf revived'}

    #hfid
    ghost = db.Column(db.String(20))

class HF_Simple_Battle(Historical_Figure):
    __mapper_args__ = {'polymorphic_identity':'hf revived'}

    #hfid group_1_hfid
    #hfid2 group_2_hfid
    #location
    #type subtype

class HF_Travel(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf travel'}

    # hfid
    # location
    returned = db.Column(db.Boolean)

class HF_Wounded(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf wounded'}

    # hfid woundee
    # hfid2 wounder
    # location
    woundee_race = db.Column(db.Integer)
    woundee_caste = db.Column(db.Integer)
    body_part = db.Column(db.Integer)
    injury_type = db.Column(db.Integer)
    part_lost = db.Column(db.Integer)

class HFs_Formed_Reputation_Relationship(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':
            'hfs formed reputation relationship'}
    #hfid1
    #hfid2
    #location
    identity_id1 = db.Column(db.Integer)
    identity_id2 = db.Column(db.Integer)
    hf_rep_1_of_2 = db.Column(db.String(20))
    hf_rep_2_of_1 = db.Column(db.String(20))

class Insurrection_Started(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'insurrection started'}

    #entity_id target_civ_id
    #site_id
    outcome = db.Column(db.String(25))

class Item_Stolen(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'item stolen'}

    # site
    # structure
    # entity
    # histfig
    # circumstance
    # circumstance_id

    ## item fields
    #item = db.Column(db.Integer)
    #mat = db.Column(db.String(20))
    #item_type = db.Column(db.String(20))
    #item_subtype = db.Column(db.String(20))
    #mat_type = db.Column(db.Integer)
    #mat_index = db.Column(db.Integer)
    #dye_mat_type = db.Column(db.Integer)
    ####

    # calc?
    # looted_from
    # looted_by
    # artifact

class Knowledge_Discovered(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'knowledge discovered'}

    knowledge = db.Column(db.String(50))
    #first = db.Column(db.Boolean)

class Masterpiece_Event(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':
                           'masterpiece event'}
    # entity_id
    # hfid
    # site
    skill_at_time = db.Column(db.Integer)

class Masterpiece_Arch_Constructed(Masterpiece_Event):
    __mapper_args__ = {'polymorphic_identity':
                           'masterpiece arch constructed'}

    building_type = db.Column(db.String(50))
    building_custom = db.Column(db.String(50))


class Masterpiece_Dye(Masterpiece_Event):
    __mapper_args__ = {'polymorphic_identity':'masterpiece dye'}

    dye_mat = db.Column(db.String(50))
    dye_mat_index = db.Column(db.String(50))

class Masterpiece_Engraving(Masterpiece_Event):
    __mapper_args__ = {'polymorphic_identity':'masterpiece engraving'}

    art_id = db.Column(db.Integer)
    art_sub_id = db.Column(db.Integer)

class Masterpiece_Food(Masterpiece_Event):
    __mapper_args__ = {'polymorphic_identity':'masterpiece food'}

class Masterpiece_Item(Masterpiece_Event):
    __mapper_args__ = {'polymorphic_identity':'masterpiece item'}

class Masterpiece_Item_Improvement(Masterpiece_Event):
    __mapper_args__ = {'polymorphic_identity':
                           'masterpiece item improvement'}
    improvement_type = db.Column(db.String(50))
    improvement_subtype = db.Column(db.String(50))
    imp_mat = db.Column(db.String(50))

    #item
    #art

class Masterpiece_Lost(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'masterpiece lost'}
    #hfid  (destroyed by)
    creation_event = db.Column(db.Integer)
    #site
    method = db.Column(db.Integer)
    # relation to event

class Merchant(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'merchant'}

    # entity_id source
    # site
    # entity_id2 destination

class New_Site_Leader(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'new site leader'}

    #entity_id attacker_civ_id
    #entity_id_2 defender_civ_id
    #site_civ_id
    # new_site_civ_id = db.Column(db.Integer)
    # hfid
    #site_id

class Occasion_Evt(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'occasion'}
    #entity_id civid
    occasion_id = db.Column(db.Integer)
    schedule_id = db.Column(db.Integer)
    #location

class Competition(Occasion_Evt):
    __mapper_args__ = {'polymorphic_identity':'competition'}

    #hfid winner
    #occasion_id = db.Column(db.Integer)
    #schedule_id = db.Column(db.Integer)

    #### List of competitors? is lookup from histfig

class Performance(Occasion_Evt):
    __mapper_args__ = {'polymorphic_identity':'performance'}

class Ceremony(Occasion_Evt):
    __mapper_args__ = {'polymorphic_identity':'ceremony'}

class Procession(Occasion_Evt):
    __mapper_args__ = {'polymorphic_identity':'procession'}

class Peace_Accepted(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'peace accepted'}
    #entity_id source
    # entity_id2 destination
    #site_id
    # topic = db.Column(db.String(30))

class Peace_Rejected(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'peace rejected'}
    #entity_id source
    # entity_id2 destination
    # site_id
    # topic = db.Column(db.String(30))

class Plundered_Site(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'plunderied site'}

    #entity_id attacker_civ_id
    #entity_id_2 defender_civ_id
    #site_civ_id

class Razed_Structure(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'razed structure'}

    #entity_id attacker_civ_id
    #entity_id_2 defender_civ_id
    #site_civ_id

class Reclaim_Site(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'reclaim site'}

    # entity_id civ_id
    # site
    # site_civ_id 

class Remove_HF_Entity_Link(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'remove hf entity link'}

    # hf
    # entity_id civ_id
    # link_type
    # position

class Remove_HF_Site_Link(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'remove hf site link'}

    # hf
    # site
    # structure
    # entity_id civ
    # link_type
    # position

class Replace_Structure(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'repalce structure'}
    # entity_id civ
    # site_civ
    # site
    # structure
    new_structure = db.Column(db.Integer)

class Site_Died(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'site died'}
    # civ_id
    # site_civ_id
    # site_id
    abandoned = db.Column(db.Boolean)

class Site_Dispute(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'site dispute'}
    #entity_id_1
    #entity_id_2
    # site
    site_id_2 = db.Column(db.Integer)
    dispute = db.Column(db.String(20))

class Site_Retired(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'site retired'}

    # civ_id
    # site_civ_id
    # site_id
    # first
   
class Site_Taken_Over(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'site taken over'}
    # entity_id atatckerciv
    # entity_id defender_civ
    # site_civ
    # new_site_civ
    # site


class Site_Tribute_Forced(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'site tribute forced'}
    # entity_id atatckerciv
    # entity_id defender_civ
    # site_civ
    # site

class Sneak_Into_Site(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'sneak into site'}
    # entity_id atatckerciv
    # entity_id defender_civ
    # site_civ
    # site

class Spotted_Leaving_Site(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'spotted leaving site'}
    # entity_id atatckerciv
    # entity_id defender_civ
    # site_civ
    # site
    #hfid spotter_hfid

class Written_Content_Composed(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'written content composed'}
    # hfid
    # circumstance
    # circumstance_id
    # reason
    # reason_id
    # wcid = db.Column(db.Integer)

