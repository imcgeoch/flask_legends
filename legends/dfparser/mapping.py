db_names = {}

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
        return self.db_mappings

    def convert(self):
        xml_dict = {k:v[0] for k, v in self.xml_dict.items()}
        xml_dict['df_world_id'] = self.world_id
        self.db_mappings[self.obj_name] = xml_dict

class Written_Content_Mapping(Mapping):

    def convert(self):
        wc_id = self.xml_dict['id'][0]

        self.db_dicts['style'] = []
        for long_style in xml_dict.get('style') or []:
            style, magnitude = long_style.split(':') 
            style_dict = {'df_world_id':self.world_id, 'content_id':wc_id,
                'style':style, 'magnitude':magnitude}
            self.db_dicts['style'].append(style_dict)

        super().convert()
