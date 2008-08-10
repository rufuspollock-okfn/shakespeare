"""
Provide an index of available material including all Milton's texts
"""
import milton.model

class MiltonIndex(object):
    """Main index of texts (MiltonIndex class).
    """

    def __init__(self):
        self.all = milton.model.Material.select(orderBy='name')


all = MiltonIndex().all
