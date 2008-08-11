"""
Provide an index of available material including all shakespeares texts
"""
import shakespeare.model

class ShakespeareIndex(object):
    """Main index of texts (ShakespeareIndex class).
    """

    def __init__(self):
        self.all = shakespeare.model.Material.query.order_by('name').all()


all = ShakespeareIndex().all
