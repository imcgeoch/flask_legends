from xml.etree.ElementTree import iterparse, XMLParser

from ..models import db, DF_World

def do_parse(fname1, fname2, worldname):
    world = DF_World(name=worldname)
    db.session.add(world)
    db.session.commit()
    world_id = world.id
    parse(fname1, "base")

def parse(filename, mode):
    parser = XMLParser('CP437')
    itr = iterparse(filename, parser=parser)

    for _, elm in itr:
        #do something

        #if in is a top-level object
        # send it to a processor
        pass

def process(elem):
    # explicit one for each object?
    # most freedom and simplest, but long and hard to maintain?
    #
    # would be something like, look up matching fn and send it off
    # that returns a list of obj, name tuples
    # this queues them to be inserted
    pass
    
