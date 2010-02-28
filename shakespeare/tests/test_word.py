import shakespeare.model.word as wordm
import shakespeare.model as model

class TestWord:
    nose_external = True

    @classmethod
    def teardown_class(self):
        for kv in model.Session.query(model.KeyValue):
            model.Session.delete(kv)
        model.Session.commit()
        model.Session.remove()

    def test_01_load_entry(self):
        # TODO: standalone test ...
        import feedparser
        entry = feedparser.FeedParserDict()
        title = u' xxx'
        name = title.strip()
        content = [{'value': u'yyy', 'language': 'en'}]
        entry.title = title
        entry.content = content
        word = wordm.load_entry(entry)
        model.Session.remove()
        word = model.Word.by_name(name)
        assert word.notes == content[0]['value'], word.notes

    def test_02_load_info_from_feed(self):
        feed_url = 'http://blog.openshakespeare.org/category/wordoftheday/?feed=atom'
        wordm.load_word_info_from_feed(feed_url)
        model.Session.remove()
        # load twice to ensure we can deal with duplicates
        wordm.load_word_info_from_feed(feed_url)
        model.Session.remove()
        current = model.Word.word_of_the_day()
        assert current.name
        assert current.notes, current

