from ..models import *

import pprint

class Connector():

    dicts = {}
    
    tables = {(Artifact, 'artifact'), (Region, 'region'),
            (Underground_Region, 'underground_region'), (Site, 'site'),
            (Structure, 'structure'),
            (Historical_Figure, 'historical_figure'), 
            (Skill, 'hf_skill'), (Entity_Link, 'entity_link'),
            (Sphere, 'sphere'), (Goal, 'goal'),
            (Journey_Pet, 'journey_pet'),
            (Interaction_Knowledge, 'interaction_knowledge'),
            (HF_Link, 'hf_link'), (Site_Link, 'site_link'),
            (Entity_Position_Link, 'entity_position_link'),
            (Entity_Reputation, 'entity_reputation'),
            (Relationship, 'relationship_profile_hf_visual'),
            (Entity_Population, 'entity_population')}

    def __init__(self, db, mode, world_id):
        # takes a connection to our db
        self.db = db
        self.mode = mode
        self.world_id = world_id
        self.pp = pprint.PrettyPrinter()
    
        self.update_fns = {'artifact':self.add_artifact, 
                  'region':self.add_simple, 
                  'underground_region':self.add_simple,
                  'site':self.add_site,
                  'historical_figure':self.add_histfig,
                  'entity_population':self.add_simple}
        self.hf_children = {('hf_skill', None),
                         ('entity_link', None),
                         ('site_link', None),
                         ('entity_position_link', None),
                         ('entity_reputation', None), 
                         ('hf_link', self.add_two_hf_child('hfid')),
                         ('relationship_profile_hf_visual',
                          self.add_two_hf_child('hf_id')),
                         ('sphere', self.make_add_hf_detail('sphere')),
                         ('goal', self.make_add_hf_detail('goal')),
                         ('journey_pet', 
                             self.make_add_hf_detail('journey_pet')),
                         ('interaction_knowledge',
                         self.make_add_hf_detail('interaction_knowledge'))}

    def add(self, name, mapping):
        # takes a dict mapping keys to fields 
        # from an xml parser, by calling appropriate helper
        #
        # converts to one or more ready-to insert dicts
        # 
        # calls bulk_insert_all if nessecary
        # (according to size or soemthing tbd)
        # print(name, mapping)

        self.update_dict(name, self.update_fns[name](mapping))

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

        for obj, key in self.tables:
            s.bulk_insert_mappings(obj, self.dicts.get(key) or {})

        s.commit()

    def get_first(self, mapping):
        return {k:v[0] for k, v in mapping.items()}  

    def add_simple(self, mapping):
        mapping = self.get_first(mapping)
        mapping['df_world_id'] = self.world_id
        return [mapping]
    
    def add_artifact(self, mapping):
        mapping = self.add_simple(mapping)[0]
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
        mapping = self.add_simple(mapping)[0]
        mapping['site_id'] = site[0]
        mapping['entity_id'] = mapping.get('entity_id') or -1
        return [mapping]
    
    def add_histfig(self, mapping):
        hfid = mapping['id'][0]

        for child_name, func in self.hf_children:
            func = func or self.add_hf_child
            children = mapping.get(child_name) or []
            for child in children:
                maps = func(child, hfid)
                self.update_dict(child_name, maps)
        
        return self.add_simple(mapping)

    def make_add_hf_detail(self, name):
        def f(item, hfid):
            mp = {'df_world_id':self.world_id, 'hfid':hfid, name:item} 
            return [mp]
        return f
     
    def add_two_hf_child(self, name):
        def f(mapping, hfid):
            mapping = self.add_simple(mapping)[0]
            mapping['hfid1'] = hfid
            mapping['hfid2'] = mapping[name]
            #mapping['rep'] = mapping.get('rep_buddy') # fix in db
            return [mapping]
        return f

    def add_hf_child(self, mapping, hfid):
        mapping = self.add_simple(mapping)[0]
        mapping['hfid'] = hfid
        return [mapping]

