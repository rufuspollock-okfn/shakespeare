"""
Provide an index of available material including all shakespeares texts
"""
import shakespeare.gutenberg

class ShakespeareIndex(object):
    """Main index of texts (ShakespeareIndex class).
    """

    def __init__(self):
        gutindex = shakespeare.gutenberg.GutenbergIndex()
        self.all = gutindex.get_shakespeare_list()
        # todo: parse it up
        self.folios = None
        self.nonfolios = None
        self.sonnets = None


all = ShakespeareIndex().all
