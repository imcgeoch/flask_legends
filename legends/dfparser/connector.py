from  .. import models as m

import pprint

orm_objects = {
        "written_content" : m.Written_Content,
        "style" : m.Style,
        "artifact" : m.Artifact,
        "site" : m.Site,
        "structure" : m.Structure,
        "historical_figure" : m.Historical_Figure,
        "hf_skill" : m.Skill,
        "entity_link" : m.Entity_Link,
        "site_link" : m.Site_Link,
        "entity_position_link" : m.Entity_Position_Link,
        "entity_reputation" : m.Entity_Reputation,
        "hf_link" : m.HF_Link,
        "relationship_profile_hf_visual": m.Relationship,
        "sphere" : m.Sphere,
        "goal" : m.Goal,
        "journey_pet" : m.Journey_Pet,
        "interaction_knowledge" : m.Interaction_Knowledge,
        "historical_event_collection" : m.Event_Collection,
        "attacking_squad" : m.Attacking_Squad,
        "defending_squad" : m.Defending_Squad,
        "historical_event" : m.Historical_Event,
        ### What's missing?
        "region" : m.Region,
        "underground_region" : m.Underground_Region,
        "entity_population" : m.Entity_Population,
        "entity" : m.Entity,
        "historical_era" : m.Historical_Era,
        "poetic_form" : m.Poetic_Form,
        "dance_form" : m.Dance_Form,
        "musical_form" : m.Musical_Form,
        # And new ones in plus
        "landmass" : m.Landmass,
        "mountain_peak" : m.Mountain_Peak,
        "world_construction" : m.World_Construction,
        "occasion" : m.Occasion,
        "schedule" : m.Schedule,
        "feature" : m.Feature,
        "entity_position" : m.Entity_Position,
        "entity_position_assignment" : m.Entity_Position_Assignment,
        "entity_entity_link" : m.Entity_Entity_Link,
        "reference" : m.Reference
        }

aux_tables = {
        "eventcol_eventcol_link" : m.collections.eventcol_eventcol_link,
        "eventcol_event_link" : m.collections.eventcol_event_link,
        "attacking_hfid" : m.collections.eventcol_attackers,
        "defending_hfid" : m.collections.eventcol_defenders,
        "noncom_hfid": m.collections.eventcol_noncoms,
        "competitor_hfid" : m.events.competitors,
        "inhabitant" : m.civilizations.inhabitants,
        "member" : m.civilizations.members
        }

# for these we insert, even thought we're in plus mode.
plus_only_objects = ["landmass", "world_construction", "mountain_peak", 
        "entity_entity_link", "entity_position", 
        "entity_position_assignment", "occasion", "schedule", "feature",
        "reference", "inhabitant", "member"]

base_only_objets = ['historical_figure', 'style']

class Connector():

    def __init__(self, db, mode, world_id, capacity=10000):
        self.db = db
        self.mode = mode
        self.world_id = world_id
        self.capacity = capacity
        self.pp = pprint.PrettyPrinter()

        self.db_mappings = {}
        self.xml_mappings = []
        
    def add_world(self):
        self.db.session.add(m.DF_World(id=self.world_id))
        self.db.session.commit()

    def add_mapping(self, xml_mapping):
        self.xml_mappings.append(xml_mapping)
        if len(self.xml_mappings) >= self.capacity:
            self.mappings_to_db()

    def convert_mappings(self):
        while self.xml_mappings:
            xml_mapping = self.xml_mappings.pop()
            xml_mapping.convert()
            if self.mode == 'update':
                xml_mapping.mask_fields()
            for name, db_mapping in xml_mapping.get_db_mappings().items():
                if name in self.db_mappings:
                    self.db_mappings[name].extend(db_mapping)
                else:
                    self.db_mappings[name] = db_mapping
    
    def insert_mappings(self):
        s = self.db.session

        while self.db_mappings:
            name, db_mapping = self.db_mappings.popitem()
            if name in orm_objects:
                s.bulk_insert_mappings(orm_objects[name], db_mapping)
            elif name in aux_tables:
                tab = aux_tables[name]
                s.execute(tab.insert(db_mapping))
        
        s.commit()
    
    def update_mappings(self):
        s = self.db.session
        mappings_to_insert = {}

        while self.db_mappings:
            name, db_mapping = self.db_mappings.popitem()
            if name in base_only_objets:
                continue
            if name in plus_only_objects:
                mappings_to_insert[name] = db_mapping
            elif name in orm_objects:
                s.bulk_update_mappings(orm_objects[name], db_mapping)
            elif name in aux_tables:
                # None right now that we would update.
                pass
        
        self.db_mappings = mappings_to_insert
        self.insert_mappings()

    def mappings_to_db(self):
        if self.mode == 'insert':
            self.convert_mappings()
            self.insert_mappings()
        elif self.mode == 'update':
            self.convert_mappings()
            self.update_mappings()
            self.insert_mappings()

