"""
Provide an index of available material including all shakespeares texts
"""
import milton.dm

class MiltonIndex(object):
    """Main index of texts (MiltonIndex class).
    """

    def __init__(self):
        self.all = milton.dm.Material.select(orderBy='name')


all = MiltonIndex().all
