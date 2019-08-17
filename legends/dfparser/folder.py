import os
import re
from glob import glob
from wand.image import Image
from xml.sax import parse as sax_parse

from .dfparser import DF_Handler 
from ..models import DF_World, db, Site_Map
from .. import create_app

IMAGE_PATH = "./images"

class DF_Parser(object):
    
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.site_maps = glob(folder_path + '*site_map*')
        self.world_maps = glob(folder_path + '*[a-z].bmp')
        self.base_xml = glob(folder_path + '*legends.xml')
        self.plus_xml = glob(folder_path + '*legends_plus.xml')
        self.plus_mode = self.plus_xml is not []

    def process(self):
        self.create_world()
        # Parse main
        self.parse_base()
        if self.plus_mode:
            parse_plus()
        # Make a location in images
        img_dir = IMAGE_PATH + self.world_id + '/'
        os.mkdir(img_dir)
        # convert and copy all site maps
        self.convert_site_maps()
        # upload paths to db
        # convert and copy all world maps
        # upload paths to db
        pass

    def create_world(self):
        world = DF_World()
        db.session.add(world)
        self.world_id = world.id

    def parse_base(self):
        filename = self.base_xml[0] 
        parse(filename, 'insert')

    def parse_plus(self)
        filename = self.plus_xml[0] 
        parse(filename, 'update')

    def parse(self, filename, mode):
        connector = Connector(db, mode, self.world_id)
        factory = Mapping_Factory(self.world_id)
        with codecs.open(filename, 'r', encoding='CP437') as infile:
            sax_parse(infile, DF_Handler(connector, factory))

    def convert_site_maps(self):
        site_num_pat = re.compile("(?<=site_map)[0-9]*(?=\.bmp)")

        site_map_objs = []
        for img_path in self.site_maps:
            site_num = site_num_pat.findall(img_path)[0]
            with Image(filename=img_path) as img:
                img.format = 'png'
                path = img_dir + 'site' + site_num
                img.save(filename=path)
                site_map = Site_Map(df_world_id=self.world_id,
                        id=int(site_num), path=path)
                site_map_objs.append(site_map)
        db.bulk_save_objects(site_maps)
        db.commit()
