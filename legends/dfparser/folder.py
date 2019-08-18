import os
import re
import codecs
from glob import glob
from wand.image import Image
from xml.sax import parse as sax_parse

from .dfparser import DF_Handler
from .mapping import Mapping_Factory
from .connector import Connector
from ..models import DF_World, db, Site_Map, World_Map
#from .. import create_app

IMAGE_PATH = "./images"

def process_directory(path):
    parser = DF_Parser(path)
    parser.process()

class DF_Parser(object):
    
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.site_maps = glob(folder_path + '*site_map*')
        self.world_maps = glob(folder_path + '*[a-z].bmp')
        self.base_xml = glob(folder_path + '*legends.xml')
        self.plus_xml = glob(folder_path + '*legends_plus.xml')
        self.plus_mode = self.plus_xml is not []

    def process(self):
        print("Creating world...")
        self.create_world()
        # Parse main
        print("Parsing base...")
        self.parse_base()
        if self.plus_mode:
            print("Parsing plus...")
            self.parse_plus()
        # Make a location in images
        print("Makign image directory...")
        self.img_dir = IMAGE_PATH + '/' + str(self.world_id) + '/'
        os.mkdir(self.img_dir)
        # convert and copy all site maps
        # and upload to db
        print("Converting site maps...")
        self.convert_site_maps()
        # convert and copy all world maps
        # and upload to db
        print("Converting world maps...")
        self.convert_world_maps()

    def create_world(self):
        world = DF_World()
        print(world)
        db.session.add(world)
        db.session.commit()
        print(world.id)
        self.world_id = world.id

    def parse_base(self):
        filename = self.base_xml[0] 
        self.parse(filename, 'insert')

    def parse_plus(self):
        filename = self.plus_xml[0] 
        self.parse(filename, 'update')

    def parse(self, filename, mode):
        connector = Connector(db, mode, self.world_id)
        factory = Mapping_Factory(self.world_id)
        with codecs.open(filename, 'r', encoding='CP437') as infile:
            sax_parse(infile, DF_Handler(connector, factory))

    def convert_site_maps(self):
        site_num_pat = re.compile("(?<=site_map-)[0-9]*(?=\.bmp)")

        site_map_objs = []

        for img_path in self.site_maps:
            site_num = site_num_pat.findall(img_path)[0]
            with Image(filename=img_path) as img:
                img.format = 'png'
                path = self.img_dir + 'site' + site_num + '.png'
                img.save(filename=path)
                site_map = Site_Map(df_world_id=self.world_id,
                        site_id=int(site_num), path=path)
                site_map_objs.append(site_map)
        db.session.bulk_save_objects(site_map_objs)
        db.session.commit()
        
    def convert_world_maps(self):
        map_type_pat = re.compile("[_a-z]+(?=\.bmp)")

        world_map_objs = []
        for img_path in self.world_maps:
            map_type = map_type_pat.findall(img_path)[0]
            with Image(filename=img_path) as img:
                img.format = 'png'
                path = self.img_dir + 'world_' + map_type + '.png'
                img.save(filename=path)
                world_map = World_Map(df_world_id=self.world_id,
                        type=map_type, path=path)
                world_map_objs.append(world_map)
        db.session.bulk_save_objects(world_map_objs)
        db.session.commit()

