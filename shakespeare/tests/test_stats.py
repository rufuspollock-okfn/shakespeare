import os
import shutil
import tempfile
import StringIO

import shakespeare.stats
import shakespeare.model as model
from shakespeare.tests import *

def stats_fixture(text):
    stats = shakespeare.stats.Stats()
    fileobj = StringIO.StringIO(text.content)
    stats.statsify(text, fileobj)

class TestStats:

    def setUp(self):
        self.stats = shakespeare.stats.Stats()
        self.text = make_fixture()
        model.Session.begin()

    def tearDown(self):
        model.Session.rollback()
        model.Session.remove()

    def test_get_stats(self):
        simpletext = 'Death death dead love loved loving'
        out = self.stats.analyze(StringIO.StringIO(simpletext))
        assert len(out) == 3
        assert out['love'] == 3
        assert out['death'] == 2
        assert out['dead'] == 1

    def test_freq_nonexistent(self):
        nonexistent_word = 'abdfakfjadf'
        freq = self.stats.freq(self.text, nonexistent_word)
        assert freq == 0
    
    def test_statsify(self):
        stats_fixture(self.text)
        word = 'summer'
        freq = self.stats.freq(self.text, word)
        assert freq == 3

    def test_text_stats(self):
        stats_fixture(self.text)

        stats = self.stats.text_stats(self.text)
        for s in stats:
            print s.word, s.freq
            if s.word == 'summer': break
        assert stats[0].word == 'and'
        assert stats[0].freq == 5
        assert stats[2].word == 'summer'
        assert stats[2].freq == 3



