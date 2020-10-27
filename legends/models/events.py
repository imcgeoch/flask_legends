from . import db 

###########################
### BEGIN HISTORICAL EVENTS
###########################
class Historical_Event(db.Model):
    __tablename__ = 'historical_events'

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE'), 
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
    site_id2 = db.Column(db.Integer)
    unit_id = db.Column(db.Integer)
    site_civ_id = db.Column(db.Integer) # local group?
    new_site_civ_id = db.Column(db.Integer)
    reason_id = db.Column(db.Integer)
    circumstance_id = db.Column(db.Integer)
    wcid = db.Column(db.Integer)
    # copied up
    building = db.Column(db.Integer)
    agreement_id = db.Column(db.Integer)
    position_profile_id = db.Column(db.Integer)
    claim = db.Column(db.Enum('heirloom', 'symbol', 'treasure', name='claim_types'))
    dest_site_id = db.Column(db.Integer)
    dest_structure_id = db.Column(db.Integer)
    dest_entity_id = db.Column(db.Integer)
    source_site_id = db.Column(db.Integer)
    source_structure_id = db.Column(db.Integer)
    source_entity_id = db.Column(db.Integer)
    from_original = db.Column(db.Boolean)
    new_artifact_id = db.Column(db.Integer)
    identity_id = db.Column(db.Integer)
    abuse_type = db.Column(db.String)
    body_state = db.Column(db.String(20))
    old_job = db.Column(db.String(20))
    new_job = db.Column(db.String(20))
    subregion_id = db.Column(db.Integer)
    state = db.Column(db.String(20))
    old_race = db.Column(db.String(40))
    new_race = db.Column(db.String(40))
    old_caste = db.Column(db.String(20))
    new_caste = db.Column(db.String(20))
    master_wcid = db.Column(db.Integer)
    race = db.Column(db.String(40))
    caste = db.Column(db.String(20))
    law_type = db.Column(db.Enum('add', 'remove', name='law_types')) #add or remove
    law = db.Column(db.String(50))
    result = db.Column(db.String(20))
    situation = db.Column(db.String(50))
    slayer_race = db.Column(db.String(40))
    slayer_caste = db.Column(db.String(20))
    slayer_item_id = db.Column(db.Integer)
    slayer_shooter_item_id = db.Column(db.Integer)
    cause = db.Column(db.String(30))
    interaction_action = db.Column(db.String(75))
    interaction_string = db.Column(db.String(150))
    source = db.Column(db.Integer)
    secret_goal = db.Column(db.String(20))
    secret_text = db.Column(db.String(50))
    pets = db.Column(db.String(50))
    unit_type = db.Column(db.String(20))
    relationship = db.Column(db.String(30))
    ghost = db.Column(db.String(20))
    subtype = db.Column(db.String(30))
    returned = db.Column(db.Boolean)
    woundee_race = db.Column(db.String(50))
    woundee_caste = db.Column(db.String(20))
    body_part = db.Column(db.Integer)
    injury_type = db.Column(db.String(20))
    part_lost = db.Column(db.String(30))
    identity_id1 = db.Column(db.Integer)
    identity_id2 = db.Column(db.Integer)
    hf_rep_1_of_2 = db.Column(db.String(20))
    hf_rep_2_of_1 = db.Column(db.String(20))
    outcome = db.Column(db.String(25))
    knowledge = db.Column(db.String(100))
    skill_at_time = db.Column(db.Integer)
    building_type = db.Column(db.String(50))
    building_custom = db.Column(db.String(50))
    dye_mat = db.Column(db.String(50))
    dye_mat_index = db.Column(db.String(50))
    art_id = db.Column(db.Integer)
    art_sub_id = db.Column(db.Integer)
    improvement_type = db.Column(db.String(50))
    improvement_subtype = db.Column(db.String(50))
    imp_mat = db.Column(db.String(50))
    creation_event = db.Column(db.Integer)
    method = db.Column(db.String(50))
    occasion_id = db.Column(db.Integer)
    schedule_id = db.Column(db.Integer)
    abandoned = db.Column(db.Boolean)
    dispute = db.Column(db.String(20))

    
    ## item fields
    item = db.Column(db.Integer)
    mat = db.Column(db.String(50))
    item_type = db.Column(db.String(20))
    item_subtype = db.Column(db.String(20))
    mat_type = db.Column(db.Integer)
    mat_index = db.Column(db.Integer)
    dye_mat_type = db.Column(db.Integer)
    ####
  
    # strings
    link_type = db.Column(db.String(30))
    reason = db.Column(db.String(50))
    position = db.Column(db.String(30))
    interaction = db.Column(db.String(50))
    action = db.Column(db.String(50))
    circumstance = db.Column(db.String(50))
    topic = db.Column(db.String(30))
    first = db.Column(db.Boolean)
    
    __mapper_args__ = {
        'polymorphic_identity':'historical_event',
        'polymorphic_on':'type'
    }

class Add_HF_Entity_Link(Historical_Event):
    
    __mapper_args__ = { 'polymorphic_identity':'add hf entity link'}

class Add_HF_HF_Link(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'add hf hf link'}

class Add_HF_Site_Link(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'add hf site link'}

class Agreement_Formed(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'agreement formed'}

class Artifact_Claim_Formed(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact claim formed'}

class Artifact_Copied(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact copied'}

class Artifact_Created(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact created'}

class Artifact_Destroyed(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact destroyed'}

class Artifact_Found(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact found'}

class Artifact_Given(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact given'}

class Artifact_Lost(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact lost'}

class Artifact_Possessed(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact possessed'}

class Artifact_Recovered(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact recovered'}

class Artifact_Stored(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'artifact stored'}

class Artifact_Transformed(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'artifact transformed'}

class Assume_Identity(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'assume identity'}

class Attacked_Site(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'attacked site'}

class Body_Abused(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'body abused'}

class Change_HF_Body_State(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'change hf body state'}

class Change_HF_Job(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'change hf job'}

class Change_HF_State(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'change hf state'}

class Change_Creature_Type(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'changed creature type'}

class Create_Entity_Position(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'create entity position'}

class Created_Site(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'created site'}

class Created_Strucure(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'created structure'}

class Created_World_Construction(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'created world construction'}

class Creature_Devoured(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'creature devoured'}
   
class Destroyed_Site(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'destroyed site'}

class Diplomat_Lost(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'diplomat lost'}

class Entity_Created(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'entity created'}

class Entity_Law(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'entity law'}

class Entity_Relocate(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'entity relocate'}

class Entity_Primary_Criminals(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'entity primary criminals'}

class Entity_Searched_Site(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'entity searched site'}

class Field_Battle(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'field battle'}

class Field_Contact(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'field contact'}

class HF_Abducted(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf abducted'}

class HF_Attacked_Site(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf attacked site'}

class HF_Confronted(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf confronted'}

class HF_Destroyed_Site(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf destroyed site'}

class HF_Died(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf died'}

class HF_Does_Interaction(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf does interaction'}

class HF_Gains_Secret_Goal(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf gains secret goal'}

class HF_Learns_Secret(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf learns secret'}

class HF_New_Pet(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf new pet'}

class HF_Prayed_Inside_Structure(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf prayed inside structure'}

class HF_Profaned_Structure(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf profaned structure'}

class HF_Reach_Summit(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf reach summit'}

class HF_Recruited_Unit_Type_For_Entity(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':
                            'hf recruited unit type for entity'}

class HF_Relationship_Denied(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf relationship denied'}

class HF_Reunion(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf reunion'}

class HF_Revived(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf revived'}

class HF_Simple_Battle(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf simple battle event'}

class HF_Travel(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf travel'}

class HF_Wounded(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf wounded'}

class HFs_Formed_Reputation_Relationship(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':
            'hfs formed reputation relationship'}

class Insurrection_Started(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'insurrection started'}

class Item_Stolen(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'item stolen'}

class Knowledge_Discovered(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'knowledge discovered'}

class Masterpiece_Event(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':
                           'masterpiece event'}

class Masterpiece_Arch_Constructed(Masterpiece_Event):
    __mapper_args__ = {'polymorphic_identity':
                           'masterpiece arch constructed'}

class Masterpiece_Dye(Masterpiece_Event):
    __mapper_args__ = {'polymorphic_identity':'masterpiece dye'}

class Masterpiece_Engraving(Masterpiece_Event):
    __mapper_args__ = {'polymorphic_identity':'masterpiece engraving'}

class Masterpiece_Food(Masterpiece_Event):
    __mapper_args__ = {'polymorphic_identity':'masterpiece food'}

class Masterpiece_Item(Masterpiece_Event):
    __mapper_args__ = {'polymorphic_identity':'masterpiece item'}

class Masterpiece_Item_Improvement(Masterpiece_Event):
    __mapper_args__ = {'polymorphic_identity':
                           'masterpiece item improvement'}

class Masterpiece_Lost(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'masterpiece lost'}
    #hfid  (destroyed by)
    #site
    # creation_event = db.Column(db.Integer)
    # method = db.Column(db.Integer)
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
    #occasion_id = db.Column(db.Integer)
    #schedule_id = db.Column(db.Integer)
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

class Peace_Rejected(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'peace rejected'}

class Plundered_Site(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'plundered site'}

class Razed_Structure(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'razed structure'}

class Reclaim_Site(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'reclaim site'}

class Remove_HF_Entity_Link(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'remove hf entity link'}

class Remove_HF_Site_Link(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'remove hf site link'}

class Replace_Structure(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'replaced structure'}
    new_structure = db.Column(db.Integer)

class Site_Died(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'site died'}

class Site_Dispute(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'site dispute'}

class Site_Retired(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'site retired'}
   
class Site_Taken_Over(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'site taken over'}

class Site_Tribute_Forced(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'site tribute forced'}

class Sneak_Into_Site(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'sneak into site'}

class Spotted_Leaving_Site(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'spotted leaving site'}

class Written_Content_Composed(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'written content composed'}

class Poetic_Form_Created(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'poetic form created'}

class Relationship_Event(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'relationship_event'}

class Remove_HF_HF_Link(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'remove hf hf link'}

class HF_Convicted(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf convicted'}

competitors = db.Table('competitors', db.metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('df_world_id',  db.Integer, db.ForeignKey('df_world.id', ondelete='CASCADE')),
        db.Column('event_id', db.Integer),
        db.Column('competitor_hfid', db.Integer),
        )

