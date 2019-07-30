from  .. import models as m

import pprint

orm_objects = {
        "written_content" : m.Written_Content,
        "style" : m.Style
        }

aux_tables = {
        "eventcol_event_link" : m.collections.eventcol_eventcol_link,
        "eventcol_event_link" : m.collections.eventcol_event_link,
        "eventcol_attackers" : m.collections.eventcol_attackers,
        "eventcol_defenders" : m.collections.eventcol_defenders,
        "eventcol_noncoms": m.collections.eventcol_noncoms
        }

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
        self.db.session.add(DF_World(id=world_id))
        self.db.session.commit()

    def add_mapping(self, xml_mapping):
        self.xml_mappings.append(xml_mapping)
        if len(self.xml_mappings) >= self.capacity:
            self.convert_and_insert_mappings()

    def convert_mappings(self):
        while self.xml_mappings:
            xml_mapping = self.xml_mappings.pop()
            xml_mapping.convert()
            for name, db_mapping in xml_mapping.get_db_mappings().items():
                if name in self.db_mappings:
                    self.db_mappings[name] = self.db_mappings[name] + db_mapping
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

    def convert_and_insert_mappings(self):
        self.convert_mappings()
        self.insert_mappings()


