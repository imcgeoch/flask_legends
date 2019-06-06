from ..models import *

import pprint

class Connector():

    dicts = {}

    def __init__(self, db, mode, world_id):
        # takes a connection to our db
        self.db = db
        self.mode = mode
        self.world_id = world_id
        self.pp = pprint.PrettyPrinter()

    def add(self, name, mapping):
        # takes a dict mapping keys to fields 
        # from an xml parser, by calling appropriate helper
        #
        # converts to one or more ready-to insert dicts
        # 
        # calls bulk_insert_all if nessecary
        # (according to size or soemthing tbd)
        # print(name, mapping)

        if name == 'artifact':
            self.update_dict('artifact', self.add_artifact(mapping))
        if name == 'region':
            self.update_dict('region', self.add_simple(mapping))
        if name == 'underground_region':
            self.update_dict('ugregion', self.add_simple(mapping))
        if name == 'site':
            self.update_dict('site', self.add_site(mapping))
        if name == 'historical_figure':
            self.update_dict('historical_figure', self.add_histfig(mapping))


    def update_dict(self, name, mapping):
        if name in self.dicts:
            self.dicts[name] += mapping
        else:
            self.dicts[name] = mapping

    def bulk_insert_all(self):
        #
        # calls db.bulk_insert for each thing in dicts
        # then clears it out
        # print(self.dicts)
        s = self.db.session
        s.bulk_insert_mappings(Artifact, self.dicts['artifact'])
        s.bulk_insert_mappings(Region, self.dicts['region'])
        s.bulk_insert_mappings(Underground_Region, self.dicts['ugregion'])
        s.bulk_insert_mappings(Site, self.dicts['site'])
        s.bulk_insert_mappings(Structure, self.dicts['structure'])
        
        s.bulk_insert_mappings(Historical_Figure, self.dicts['historical_figure'])
        s.bulk_insert_mappings(Skill, self.dicts['hf_skill'])
        s.bulk_insert_mappings(Entity_Link, self.dicts['entity_link'])

        s.commit()

    def get_first(self, mapping):
        return {k:v[0] for k, v in mapping.items()}  

    def add_simple(self, mapping):
        mapping = self.get_first(mapping)
        mapping['df_world_id'] = self.world_id
        return [mapping]
    
    def add_artifact(self, mapping):
        mapping = self.get_first(mapping)
        mapping['df_world_id'] = self.world_id
        mapping['written_content_id'] = \
            mapping.get('page_written_content_id') or \
            mapping.get('writing_written_contnet_id')
        return [mapping]

    def add_site(self, mapping):
        struc_map = mapping.get('structure') or [] 
        for m in struc_map:
            self.update_dict('structure', 
                             self.add_structure(m, mapping['id']))
        return self.add_simple(mapping)

    def add_structure(self, mapping, site):
        mapping = self.get_first(mapping)
        mapping['site_id'] = site[0]
        mapping['entity_id'] = mapping.get('entity_id') or -1
        mapping['df_world_id'] = self.world_id
        return [mapping]
    
    def add_histfig(self, mapping):
        hf_skill_map = mapping.get('hf_skill') or []
        entity_link_map = mapping.get('entity_link') or []
        for m in hf_skill_map: 
            self.update_dict('hf_skill', 
                             self.add_hf_detail(m, mapping['id'][0]))
        for m in entity_link_map: 
            self.update_dict('entity_link', 
                             self.add_hf_detail(m, mapping['id'][0]))
        return self.add_simple(mapping)

    def add_hf_detail(self, mapping, hfid):
        mapping = self.get_first(mapping)
        mapping['hfid'] = hfid
        mapping['df_world_id'] = self.world_id
        return [mapping]

