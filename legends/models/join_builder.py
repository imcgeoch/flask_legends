def join_builder(obj1, obj2, *field_names):
    field_names += (("df_world_id", "df_world_id"),)
    equalities = ["%s.%s == %s.%s" % (obj1, f1, obj2, f2) for f1, f2 in field_names]
    return "and_( %s )" % (', '.join(equalities))

def table_join_builder(obj1, obj2, *field_names):
    field_names += (("df_world_id", "df_world_id"),)
    equalities = ["%s.%s == %s.c.%s" % (obj1, f1, obj2, f2) for f1, f2 in field_names]
    return "and_( %s )" % (', '.join(equalities))
