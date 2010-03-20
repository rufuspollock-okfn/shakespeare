# -*- coding: utf8 -*-
'''Import content from external (atom) feeds.

This is particularly useful for allowing people to edit content in, e.g.,
wordpress and for us to then import it.
'''
import feedparser
import shakespeare.model as model

class WorkIntroductionLoader(object):
    '''Load work introductions from a set of entries supplied via an (atom)
    feed.
    '''
    cfg_key = u'feed.work_introductions'

    def load_feed(self, feed_url=None):
        '''
        @param feed_url: if not provided using value from config key specified
        by cfg_key.
        '''
        if not feed_url:
            # minimize dependency on pylons
            from pylons import config
            feed_url = config.get(self.cfg_key, '')
        if not feed_url:
            msg = 'Need a feed_url - not specified in config (%s)' % self.cfg_key
            raise ValueError(msg)
        # handle possible wordpress pagination
        feed = feedparser.parse(feed_url)
        results = []
        def _get_link(e):
            return e.links[0].href if e.links else ''
        for idx, entry in enumerate(feed.entries):
            res = self.load_entry(entry)
            results.append([_get_link(entry), res])
        model.Session.commit()
        return results

    def load_entry(self, entry):
        '''Load a feedparser entry into KeyValue objects.
        
        @return: work object if found a match or info string if no match.

        TODO: (?) deal with wordpress pagination of feeds (defaults to 10). Can
        get pages via paged query parameter e.g. to get second page:
        http://.../fed/atom/?paged=2
        '''
        title = entry.title.lower().strip()
        # may be of form "Introduction: Hamlet"
        if ':' in title:
            title = title.split(':')[1].strip()
        title = unescape(title)
        # HACK: annoyingly wordpress changes "'" to "’"
        title = title.replace(u'’', "'")
        content = entry.content[0]['value']
        content = unescape(content)
        work = model.Session.query(model.Work).filter(model.Work.title.ilike(title)).first()
        if work is None:
            res = 'NO WORK FOUND'
        else:
            work.notes = content
            res = work
        return res

##
# from http://effbot.org/zone/re-sub.htm#unescape-html
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.
import re, htmlentitydefs

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)
