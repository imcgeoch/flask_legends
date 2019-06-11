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
        tables = {(Artifact, 'artifact'), (Region, 'region'),
            (Underground_Region, 'ugregion'), (Site, 'site'),
            (Structure, 'structure'),
            (Historical_Figure, 'historical_figure'), 
            (Skill, 'hf_skill'), (Entity_Link, 'entity_link'),
            (Sphere, 'sphere'), (Goal, 'goal'),
            (Journey_Pet, 'journey_pet'),
            (Interaction_Knowledge, 'interaction_knowledges'),
            (HF_Link, 'hf_link'), (Site_Link, 'site_link'),
            (Entity_Position_Link, 'entity_position_link'),
            (Entity_Reputation, 'entity_reputation'),
            (Relationship, 'relationship')}

        for obj, key in tables:
            s.bulk_insert_mappings(obj, self.dicts[key])

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
        site_link_map = mapping.get('site_link') or []
        entity_position_link_map = mapping.get('entity_position_link') or []
        entity_reputation_map = mapping.get('entity_reputation') or []
        hf_link_map = mapping.get('hf_link') or []
        relationship_map = mapping.get('relationship_profile_hf_visual')\
                or []
        spheres = mapping.get('sphere') or []
        goals = mapping.get('goal') or []
        journey_pets = mapping.get('journey_pet') or []
        int_know = mapping.get('interaction_knowledge') or []


        for m in hf_skill_map: 
            self.update_dict('hf_skill', 
                             self.add_hf_detail(m, mapping['id'][0]))
        for m in entity_link_map: 
            self.update_dict('entity_link', 
                             self.add_hf_detail(m, mapping['id'][0]))
        for m in site_link_map: 
            self.update_dict('site_link', 
                             self.add_hf_detail(m, mapping['id'][0]))
        for m in entity_position_link_map: 
            self.update_dict('entity_position_link', 
                             self.add_hf_detail(m, mapping['id'][0]))
        for m in entity_reputation_map:
            self.update_dict('entity_reputation', 
                    self.add_hf_detail(m, mapping['id'][0]))
        for m in hf_link_map:
            self.update_dict('hf_link', 
                             self.add_hf_link(m, mapping['id'][0]))
        for m in relationship_map:
            self.update_dict('relationship', 
                             self.add_hf_relationship(m, mapping['id'][0]))
        self.add_sphere(spheres, mapping['id'][0])
        self.add_goal(goals, mapping['id'][0])
        self.add_pet(journey_pets, mapping['id'][0])
        self.add_int_know(int_know, mapping['id'][0])
        return self.add_simple(mapping)

    def add_sphere(self, lst, hfid):
        maps = [{'df_world_id':self.world_id, 'hfid':hfid, 
                  'sphere':sphere} for sphere in lst]
        self.update_dict('sphere', maps)
    
    def add_goal(self, lst, hfid):
        maps = [{'df_world_id':self.world_id, 'hfid':hfid, 
                  'goal':goal} for goal in lst]

        self.update_dict('goal', maps)
    def add_pet(self, lst, hfid):
        maps = [{'df_world_id':self.world_id, 'hfid':hfid, 
                  'journey_pet':pet} for pet in lst]

        self.update_dict('journey_pet', maps)
    def add_int_know(self, lst, hfid):
        maps = [{'df_world_id':self.world_id, 'hfid':hfid, 
                  'interaction_knowledge':know} for know in lst]

        self.update_dict('interaction_knowledges', maps)
    def add_hf_link(self, mapping, hfid):
        mapping = self.get_first(mapping)
        mapping['hfid1'] = hfid
        mapping['hfid2'] = mapping['hfid']
        mapping['df_world_id'] = self.world_id
        return [mapping]
    
    def add_hf_relationship(self, mapping, hfid):
        mapping = self.get_first(mapping)
        mapping['hfid1'] = hfid
        mapping['hfid2'] = mapping['hf_id']
        mapping['rep'] = mapping.get('rep_buddy') # fix in db
        mapping['df_world_id'] = self.world_id
        return [mapping]

    def add_hf_detail(self, mapping, hfid):
        mapping = self.get_first(mapping)
        mapping['hfid'] = hfid
        mapping['df_world_id'] = self.world_id
        return [mapping]

