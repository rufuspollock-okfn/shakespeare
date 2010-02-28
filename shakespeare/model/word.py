from keyvalue import KeyValue
from meta import Session

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

def load_entry(entry):
    '''Load a feedparser entry into KeyValue objects.
    
    @return: list of KeyValue objects created.
    '''
    name = entry.title.lower().strip()
    # may be of form "Word of the Day: Baker"
    if ':' in name:
        name = name.split(':')[1].strip()
    ns = u'word'
    objid = name
    notes = entry.content[0]['value']
    key=u'notes'
    # upsert ...
    kv = KeyValue(ns=ns, object_id=objid, key=key, value=notes)
    merged = Session.merge(kv)
    Session.commit()
    return [merged]

def load_word_info_from_feed(feed_url=None):
    '''Load word information (e.g. notes) from a set of entries supplied via an
    (atom) feed.

    @parm feed_url: if not provided using value from config
        "word_of_the_day.feed"
    '''
    if not feed_url:
        from pylons import config
        cfg_key = 'word_of_the_day.feed'
        feed_url = config.get(cfg_key, '')
    if not feed_url:
        msg = 'Need a feed_url - not specified in config (%s)' % cfg_key
        raise ValueError(msg)
    # do not make a global dependency
    import feedparser
    feed = feedparser.parse(feed_url)
    for idx, entry in enumerate(feed.entries):
        out = load_entry(entry)
        if idx == 0:
            word = out[0].key
            # update current wotd to latest entry (first one)
            setting = KeyValue(ns=u'settings', object_id=u'word_of_the_day',
                    key=u'current', value=word)
            merged = Session.merge(setting)
            Session.commit()

