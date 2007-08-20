"""
Provide an index of available material including all shakespeares texts
"""
import shakespeare.dm

class ShakespeareIndex(object):
    """Main index of texts (ShakespeareIndex class).
    """

    def __init__(self):
        self.all = shakespeare.dm.Material.select(orderBy='name')


all = ShakespeareIndex().all
