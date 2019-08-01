db_names = {}

extract_values = lambda xml_dict: {k:v[0] for k, v in xml_dict.items()}


class Mapping(object):
    
    def __init__(self, xml_dict, obj_name, world_id):
        self.xml_dict = xml_dict
        self.obj_name = obj_name
        self.world_id = world_id
        self.db_dicts = {}

    def get_db_mappings(self):
        '''
        Return the a dictionary containing all the db mappings
        created from this object.

        '''
        return self.db_dicts

    def convert(self):
        db_dict = extract_values(self.xml_dict) 
        db_dict['df_world_id'] = self.world_id
        self.db_dicts[self.obj_name] = [db_dict]

    def convert_detail(self, name, detail_dict_list, 
                       *rewrite_list, **parent_keys):
        for old, new in rewrite_list:
            for detail_dict in detail_dict_list:
                detail_dict[new] = detail_dict.pop(old, None)
        self.db_dicts[name] = [{**extract_values(detail_dict),
            'df_world_id' : self.world_id, **parent_keys}
            for detail_dict in detail_dict_list]

    def convert_list(self, detail_name, detail_list, **parent_keys):
        self.db_dicts[detail_name] = [{"df_world_id" : self.world_id,
                                       detail_name : detail,
                                       **parent_keys}
                                       for detail in detail_list]

class Artifact_Mapping(Mapping):
    
    def convert(self):
        super().convert()

        self.db_dicts['artifact'][0]['written_content_id'] = \
            self.db_dicts['artifact'][0].get('page_written_content_id') or \
            self.db_dicts['artifact'][0].get('writing_written_content_id')

class Site_Mapping(Mapping):

    def convert(self):
        site_id = self.xml_dict['id'][0]
        structures = self.xml_dict.get('structure') or []
        self.convert_detail('structure', structures, site_id=site_id)
        
        super().convert()

class Histfig_Mapping(Mapping):

    def convert(self):
        hfid = self.xml_dict['id'][0]
        
        # these ones are simple, multi-field, details
        simple_details = ['hf_skill', 'entity_link','site_link', 
                          'entity_position_link', 'entity_reputation']
        for detail_name in simple_details:
            detail = self.xml_dict.get(detail_name) or []
            self.convert_detail(detail_name, detail, hfid=hfid)

        # hf_link and relationship_profile_hf_visual require changing
        # the name of the other hf for the db.
        hf_links = self.xml_dict.get('hf_link') or []
        self.convert_detail('hf_link', hf_links, ('hfid', 'hfid2'), hfid1=hfid)
        hf_rel_profs = self.xml_dict.get('relationship_profile_hf_visual') or []
        self.convert_detail('relationship_profile_hf_visual', hf_rel_profs,
                            ('hf_id', 'hfid2'), hfid1=hfid)

        # these ones are single values, of which there may be more than
        # one for a given histfig
        one_field_details = ['sphere', 'goal', 'journey_pet', 
                             'interaction_knowledge']
        for detail_name in one_field_details:
            detail_list = self.xml_dict.get(detail_name) or []
            self.convert_list(detail_name, detail_list, hfid=hfid)
        
        super().convert()


class Written_Content_Mapping(Mapping):

    def convert(self):
        wc_id = self.xml_dict['id'][0]

        self.db_dicts['style'] = []
        for long_style in self.xml_dict.get('style') or []:
            style, magnitude = long_style.split(':') 
            style_dict = {'df_world_id':self.world_id, 'content_id':wc_id,
                'style':style, 'magnitude':magnitude}
            self.db_dicts['style'].append(style_dict)

        super().convert()


class Mapping_Factory(object):
    mapping_by_name = { "written_content" : Written_Content_Mapping,
                        "artifact" : Artifact_Mapping,
                        "site" : Site_Mapping,
                        "historical_figure" : Histfig_Mapping}

    def __init__(self, world_id):
        self.world_id = world_id

    def from_dict(self, name, xml_dict):
        return self.mapping_by_name[name](xml_dict, name, self.world_id)
