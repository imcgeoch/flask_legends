from . import db

class Artifact(db.Model):
    __tablename__ = 'artifacts'

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    name_string = db.Column(db.String(50))
    page_number = db.Column(db.Integer)
    # page_written_content_id = db.Column(db.Integer) redundant scroll vs book
    written_content_id = db.Column(db.Integer)
    holder_hfid = db.Column(db.Integer)
    site_id = db.Column(db.Integer)
    structure_local_id = db.Column(db.Integer)

    item_type = db.Column(db.String(20))
    item_subtype = db.Column(db.String(20))
    item_description = db.Column(db.String(200))
    mat = db.Column(db.String(20))

    __table_args__ = (db.ForeignKeyConstraint([df_world_id, holder_hfid],
                                 ['historical_figures.df_world_id',
                                  'historical_figures.id']), {})

    # add lookup to written_contents

    def __repr__(self):
        return "<Artifact %s>" % (self.name)


class Written_Content(db.Model):
    __tablename__ = 'written_contents'
    
    forms = ['musical composition', 'choreography', 'poem', 'guide',
             'essay', 'manual', 'cultural history', 'star chart', 
             'letter', 'short story', 'cultural composition', 'novel', 
             'autobiography', 'comparative biography', 'biography']

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    form = db.Column(db.Enum(*forms))
    form_id = db.Column(db.Integer) # use primaryjoin with form_id == TYPE 
    author_hfid = db.Column(db.Integer)
    author_roll = db.Column(db.Integer)

    styles = db.relationship('Style')
    
    __table_args__ = (db.ForeignKeyConstraint([df_world_id, author_hfid],
                                 ['historical_figures.df_world_id',
                                  'historical_figures.id']), {})

class Style(db.Model):
    __tablename__ = 'styles'

    id = db.Column(db.Integer, primary_key=True)
    df_world_id = db.Column(db.Integer)
    content_id = db.Column(db.Integer)
    style = db.Column(db.String(10)) #should be enum
    magnitude = db.Column(db.Integer)
    __table_args__ = (db.ForeignKeyConstraint([df_world_id, content_id],
                                 [Written_Content.df_world_id,
                                  Written_Content.id]), {})

class Musical_Form(db.Model):
    __tablename__ = 'musical_forms'
    
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text())

class Poetic_Form(db.Model):
    __tablename__ = 'poetic_forms'
    
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'), 
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text())

class Dance_Form(db.Model):
    __tablename__ = 'dance_forms'
    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'),
                            primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text())

class Historical_Era(db.Model):
    __tablename__ = 'historical_eras'

    df_world_id = db.Column(db.Integer, db.ForeignKey('df_world.id'),
                            primary_key=True)
    name = db.Column(db.String(50), primary_key=True)
    start_year = db.Column(db.Integer)

    def __repr__(self):
        return "<Historical Era %s>" % (self.name)
