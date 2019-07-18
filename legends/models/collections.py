from . import db

## TODO : Squad!

eventcol_event_link = db.Table('eventcol_event_link', db.metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('df_world_id', db.Integer),
        db.Column('event_id', db.Integer),
        db.Column('eventcol_id', db.Integer),
        db.ForeignKeyConstraint(['df_world_id', 'eventcol_id'],
                                ['event_collections.df_world_id',
                                 'event_collections.id']),
        db.ForeignKeyConstraint(['df_world_id', 'event_id'],
                                ['historical_events.df_world_id',
                                 'historical_events.id'])
        )

eventcol_eventcol_link = db.Table('eventcol_eventcol_link', db.metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('df_world_id', db.Integer),
        db.Column('eventcol_id1', db.Integer),
        db.Column('eventcol_id2', db.Integer),
        db.ForeignKeyConstraint(['df_world_id', 'eventcol_id1'],
                                ['event_collections.df_world_id',
                                 'event_collections.id']),
        db.ForeignKeyConstraint(['df_world_id', 'eventcol_id2'],
                                ['event_collections.df_world_id',
                                 'event_collections.id']),
        )

eventcol_attackers = db.Table('eventcol_attackers', db.metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('df_world_id', db.Integer),
        db.Column('eventcol_id', db.Integer),
        db.Column('hfid', db.Integer),
        db.ForeignKeyConstraint(['df_world_id', 'hfid'],
                                ['historical_figures.df_world_id',
                                 'historical_figures.id']),
        db.ForeignKeyConstraint(['df_world_id', 'eventcol_id'],
                                ['event_collections.df_world_id',
                                 'event_collections.id'])
        )
eventcol_defenders = db.Table('eventcol_defenders', db.metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('df_world_id', db.Integer),
        db.Column('eventcol_id', db.Integer),
        db.Column('hfid', db.Integer),
        db.ForeignKeyConstraint(['df_world_id', 'hfid'],
                                ['historical_figures.df_world_id',
                                 'historical_figures.id']),
        db.ForeignKeyConstraint(['df_world_id', 'eventcol_id'],
                                ['event_collections.df_world_id',
                                 'event_collections.id'])
        )
eventcol_noncoms = db.Table('eventcol_noncoms', db.metadata,
        db.Column('id', db.Integer, primary_key=True),
        db.Column('df_world_id', db.Integer),
        db.Column('eventcol_id', db.Integer),
        db.Column('hfid', db.Integer),
        db.ForeignKeyConstraint(['df_world_id', 'hfid'],
                                ['historical_figures.df_world_id',
                                 'historical_figures.id']),
        db.ForeignKeyConstraint(['df_world_id', 'eventcol_id'],
                                ['event_collections.df_world_id',
                                 'event_collections.id'])
        )

class Event_Collection(db.Model):
    __tablename__ = 'event_collections'
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)

    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    start_seconds72 = db.Column(db.Integer)
    end_seconds72 = db.Column(db.Integer)

    subregion_id = db.Column(db.Integer)
    coords       = db.Column(db.String(20))
    feature_layer_id = db.Column(db.Integer)
    
    name = db.Column(db.String(50))
    adjective = db.Column(db.String(50))
    type = db.Column(db.String(20))
    ordinal = db.Column(db.Integer)
    occasion_id = db.Column(db.Integer)

    site_id = db.Column(db.Integer)
    
    # Eventcol relations
    parent_eventcol = db.Column(db.Integer)
    war_eventcol = db.synonym(parent_eventcol)

    #Entity related
    entity_id = db.Column(db.Integer)
    entity_id2 = db.Column(db.Integer)

    civ_id = db.synonym(entity_id)
    attacking_enid = db.synonym(entity_id)
    defending_enid = db.synonym(entity_id2)

    __table_args__ = (db.ForeignKeyConstraint(
        [df_world_id, parent_eventcol], [df_world_id, id]), 
#                      db.ForeignKeyConstraint(
#        [df_world_id, entity_id], ['entities.df_world_id', 'entities.id']), 
#                      db.ForeignKeyConstraint(
#        [df_world_id, entity_id2], ['entities.df_world_id', 'entities.id']),
                      db.ForeignKeyConstraint(
        [df_world_id, site_id], ['sites.df_world_id', 'sites.id']), 
        {})

    children = db.relationship('Event_Collection', remote_side=[id], 
                               backref='parent', viewonly=True)
    linked_collections = db.relationship('Event_Collection',
      secondary='eventcol_eventcol_link',backref='parent_linked',
      foreign_keys='eventcol_eventcol_link.c.eventcol_id1', viewonly=True)

    linked_events = db.relationship('Historical_Event', viewonly=True, 
            secondary='eventcol_event_link', backref='collections')

    attackers = db.relationship('Historical_Figure', viewonly=True,
            secondary='eventcol_attackers', backref='attacker_collections')
    defender = db.relationship('Historical_Figure', viewonly=True,
            secondary='eventcol_defenders', backref='defender_collections')
    noncoms = db.relationship('Historical_Figure', viewonly=True,
            secondary='eventcol_attackers', backref='noncom_collections')



