from shakespeare.tests import *
import shakespeare.model as model
import shakespeare.lib.feed as feed

class TestFeed:
    nose_external = True

    @classmethod
    def setup_class(self):
        TestData.make_fixture()

    @classmethod
    def teardown_class(self):
        TestData.remove_fixtures()

    def test_01_load_entry(self):
        import feedparser
        entry = feedparser.FeedParserDict()
        title = u'Introduction: Sonnet 18'
        name = title.strip()
        content = [{'value': u'yyy', 'language': 'en'}]
        entry.title = title
        entry.content = content

        loader = feed.WorkIntroductionLoader()
        work = loader.load_entry(entry)
        assert work.name == 'test_sonnet18', work
        model.Session.commit()
        model.Session.remove()
        work = model.Work.by_name(TestData.name)
        assert work.notes == content[0]['value'], work.notes

    # TODO: re-enable
    def _test_02_load_feed(self):
        '''Disabled as cannot work how to set content items on an entry ...'''
        import webhelpers.feedgenerator as feedgenerator
        atomfeed = feedgenerator.Atom1Feed(
            title=u'Testing',
            link=u'',
            description=u'',
            language=u'en',
        )
        # TODO: cannot work out how to set content items ...
        atomfeed.add_item(title='Hello', link=u'testing',
                description='Testing.')
        feeddata = atomfeed.writeString('utf-8')

        loader = feed.WorkIntroductionLoader()
        results = loader.load_feed(feeddata)
        assert len(results) == 1, results


