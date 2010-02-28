from keyvalue import KeyValue

class Word(object):
    def __init__(self, name, **kwargs):
        self.name = name
        self.notes = u''
        for k,v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def by_name(self, name):
        kvs = KeyValue.query.filter_by(ns=u'word').filter_by(object_id=name).all()
        # encode as keywords in kwargs must be strings ...
        kwargs = dict([ (kv.key.encode('utf8'),kv.value) for kv in kvs ])
        return Word(name, **kwargs)

