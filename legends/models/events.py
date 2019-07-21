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
    race = db.Column(db.String(20))
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
    interaction_action = db.Column(db.String(20))
    interaction_string = db.Column(db.String(20))
    source = db.Column(db.Integer)
    secret_goal = db.Column(db.String(20))
    secret_text = db.Column(db.String(50))
    pets = db.Column(db.String(50))
    unit_type = db.Column(db.String(20))
    relationship = db.Column(db.String(20))
    ghost = db.Column(db.String(20))
    subtype = db.Column(db.String(30))
    returned = db.Column(db.Boolean)
    woundee_race = db.Column(db.Integer)
    woundee_caste = db.Column(db.Integer)
    body_part = db.Column(db.Integer)
    injury_type = db.Column(db.Integer)
    part_lost = db.Column(db.Integer)
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
    method = db.Column(db.Integer)
    occasion_id = db.Column(db.Integer)
    schedule_id = db.Column(db.Integer)
    abandoned = db.Column(db.Boolean)
    dispute = db.Column(db.String(20))

    
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
    # position = db.Column(db.String(20))
    
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
    # building = db.Column(db.Integer)

class Agreement_Formed(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'agreement formed'}

    #agreement_id = db.Column(db.Integer)
    #hfid = db.Column(db.Integer)
    #site_id = db.Column(db.Integer)
    #artifact_id = db.Column(db.Integer)

    #concluder_hfid, subject_id, reason in java but not seen in xml


class Artifact_Claim_Formed(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact claim formed'}

    #hfid = db.Column(db.Integer)
    #artifact_id = db.Column(db.Integer)
    #entity_id = db.Column(db.Integer)
    #position_profile_id = db.Column(db.Integer)
    #claim = db.Column(db.Enum('heirloom', 'symbol', 'treasure'))

class Artifact_Copied(Historical_Event):
    __mapper_args__ = { 'polymorphic_identity':'artifact copied'}

    # artifact_id = db.Column(db.Integer)
    #dest_site_id = db.Column(db.Integer)
    #dest_structure_id = db.Column(db.Integer)
    #dest_entity_id = db.Column(db.Integer)
    #source_site_id = db.Column(db.Integer)
    #source_structure_id = db.Column(db.Integer)
    #source_entity_id = db.Column(db.Integer)
    #from_original = db.Column(db.Boolean)

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
    # new_artifact_id = db.Column(db.Integer)
    # artifact_id
    # unit_id
    # site_id
    # hfid

class Assume_Identity(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'assume identity'}

    #hfid
    #identity_id = db.Column(db.Integer)
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
    # abuse_type = db.Column(db.Integer)
    #site 

class Change_HF_Body_State(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'change hf body state'}
    #hfid
    #body_state = db.Column(db.String(20))
    #siteid
    #building_id = db.Column(db.Integer)

class Change_HF_Job(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'change hf job'}
    #    old_job = db.Column(db.String(20))
    #    new_job = db.Column(db.String(20))
    #hfid

class Change_HF_State(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'change hf state'}
    #subregion_id = db.Column(db.Integer)
    #hfid = db.Column(db.Integer)
    #state = db.Column(db.String(20))

class Change_Creature_Type(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'change creature type'}
    #hfid1 changer
    #hfid2 changee
    #old_race = db.Column(db.String(20))
    #new_race = db.Column(db.String(20))
    #old_caste = db.Column(db.String(20))
    #new_caste = db.Column(db.String(20))


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
    # master_wcid = db.Column(db.Integer)
    # site_id2 = db.Column(db.Integer)

class Creature_Devoured(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'creature devoured'}

    # hfid1 victim 
    # hfid2 eater 
    # entity
    # site

    # race = db.Column(db.String(20))
    # caste = db.Column(db.String(20))
   
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
    #    law_type = db.Column(db.Enum('add', 'remove')) #add or remove
    #    law = db.Column(db.String(50))

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
    # result = db.Column(db.String(20))

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
    # situation = db.Column(db.String(50))
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
    #    slayer_race = db.Column(db.String(20))
    #    slayer_caste = db.Column(db.String(20))
    #    slayer_item_id = db.Column(db.Integer)
    #    slayer_shooter_item_id = db.Column(db.Integer)
    #    cause = db.Column(db.String(20))

class HF_Does_Interaction(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf does interaction'}

    #hfid doer_hfid
    #hfid target_hfid
    #location
    #interaction = db.Column(db.String(50))
    # interaction_action = db.Column(db.String(20))
    #  interaction_string = db.Column(db.String(20))
    #  source = db.Column(db.Integer)
class HF_Gains_Secret_Goal(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf gains secret goal'}

    #hfid
    #secret_goal = db.Column(db.String(20))

class HF_Learns_Secret(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf learns secret'}

    #hifd studet
    #hfid teacher
    #artifact_id
    #interaction = db.Column(db.String(50))
    # secret_text = db.Column(db.String(50))

class HF_New_Pet(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf new pet'}
    # hfid group/grouphfid
    # pets = db.Column(db.String(50))
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
    # unit_type = db.Column(db.String(20))

class HF_Relationship_Denied(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf relationship denied'}

    #hdif seeker_hfid
    #hfid2 target_hfid
    #relationship = db.Column(db.String(20))
    #reason
    #reason_id = db.Column(db.Integer)

class HF_Reunion(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf reunion'}

    #hfid group1hfid
    #relationship with hfid (multiple targetsi possible)

class HF_Revived(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf revived'}

    #hfid
    # ghost = db.Column(db.String(20))

class HF_Simple_Battle(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf simple battle event'}

    #hfid group_1_hfid
    #hfid2 group_2_hfid
    #location
    #type subtype

class HF_Travel(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf travel'}

    # hfid
    # location
    # returned = db.Column(db.Boolean)

class HF_Wounded(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'hf wounded'}

    # hfid woundee
    # hfid2 wounder
    # location
    # woundee_race = db.Column(db.Integer)
    # woundee_caste = db.Column(db.Integer)
    # body_part = db.Column(db.Integer)
    # injury_type = db.Column(db.Integer)
    # part_lost = db.Column(db.Integer)

class HFs_Formed_Reputation_Relationship(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':
            'hfs formed reputation relationship'}
    #hfid1
    #hfid2
    #location
    # identity_id1 = db.Column(db.Integer)
    # identity_id2 = db.Column(db.Integer)
    # hf_rep_1_of_2 = db.Column(db.String(20))
    # hf_rep_2_of_1 = db.Column(db.String(20))

class Insurrection_Started(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'insurrection started'}

    #entity_id target_civ_id
    #site_id
    #outcome = db.Column(db.String(25))

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

    # knowledge = db.Column(db.String(50))
    #first = db.Column(db.Boolean)

class Masterpiece_Event(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':
                           'masterpiece event'}
    # entity_id
    # hfid
    # site
    # skill_at_time = db.Column(db.Integer)

class Masterpiece_Arch_Constructed(Masterpiece_Event):
    __mapper_args__ = {'polymorphic_identity':
                           'masterpiece arch constructed'}

    #building_type = db.Column(db.String(50))
    #building_custom = db.Column(db.String(50))


class Masterpiece_Dye(Masterpiece_Event):
    __mapper_args__ = {'polymorphic_identity':'masterpiece dye'}

    # dye_mat = db.Column(db.String(50))
    # dye_mat_index = db.Column(db.String(50))

class Masterpiece_Engraving(Masterpiece_Event):
    __mapper_args__ = {'polymorphic_identity':'masterpiece engraving'}

    #art_id = db.Column(db.Integer)
    #art_sub_id = db.Column(db.Integer)

class Masterpiece_Food(Masterpiece_Event):
    __mapper_args__ = {'polymorphic_identity':'masterpiece food'}

class Masterpiece_Item(Masterpiece_Event):
    __mapper_args__ = {'polymorphic_identity':'masterpiece item'}

class Masterpiece_Item_Improvement(Masterpiece_Event):
    __mapper_args__ = {'polymorphic_identity':
                           'masterpiece item improvement'}
    # improvement_type = db.Column(db.String(50))
    # improvement_subtype = db.Column(db.String(50))
    # imp_mat = db.Column(db.String(50))

    #item
    #art

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
    __mapper_args__ = {'polymorphic_identity':'plundered site'}

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
    # abandoned = db.Column(db.Boolean)

class Site_Dispute(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'site dispute'}
    #entity_id_1
    #entity_id_2
    # site
    # site_id_2 = db.Column(db.Integer)
    # dispute = db.Column(db.String(20))

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

class Poetic_Form_Created(Historical_Event):
    __mapper_args__ = {'polymorphic_identity':'poetic form created'}


competitors = db.Table('competitors', db.metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('df_world_id', db.Integer),
        db.Column('event_id', db.Integer),
        db.Column('competitor_hfid', db.Integer),
        )

