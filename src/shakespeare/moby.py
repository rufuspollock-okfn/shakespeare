"""
Obtain and import the Moby/Bosak xml-i-fied versions of shakespeare's plays
available from:

    <http://www.ibiblio.org/xml/examples/shakespeare/>
"""

# just extract by hand from the above webpage
# vim regex used to do this
# s:^.*href="\([^"]*\)">\([^<]*\)</a>:    ("\2",^M         'http\://www.ibiblio.org/xml/examples/shakespeare/\1'),:g

index = [
    ("All's Well That Ends Well",
        'http://www.ibiblio.org/xml/examples/shakespeare/all_well.xml'),
    ("As You Like It",
        'http://www.ibiblio.org/xml/examples/shakespeare/as_you.xml'),
    ("Antony and Cleopatra",
        'http://www.ibiblio.org/xml/examples/shakespeare/a_and_c.xml'),
    ("A Comedy of Errors",
        'http://www.ibiblio.org/xml/examples/shakespeare/com_err.xml'),
    ("Coriolanus",
        'http://www.ibiblio.org/xml/examples/shakespeare/coriolan.xml'),
    ("Cymbeline",
        'http://www.ibiblio.org/xml/examples/shakespeare/cymbelin.xml'),
    ("A Midsummer Night's Dream",
        'http://www.ibiblio.org/xml/examples/shakespeare/dream.xml'),
    ("Hamlet",
        'http://www.ibiblio.org/xml/examples/shakespeare/hamlet.xml'),
    ("Henry IV, Part I",
        'http://www.ibiblio.org/xml/examples/shakespeare/hen_iv_1.xml'),
    ("Henry IV, Part II",
        'http://www.ibiblio.org/xml/examples/shakespeare/hen_iv_2.xml'),
    ("Henry V",
        'http://www.ibiblio.org/xml/examples/shakespeare/hen_v.xml'),
    ("Henry VIII",
        'http://www.ibiblio.org/xml/examples/shakespeare/hen_viii.xml'),
    ("Henry VI, Part 1",
        'http://www.ibiblio.org/xml/examples/shakespeare/hen_vi_1.xml'),
    ("Henry VI, Part 2",
        'http://www.ibiblio.org/xml/examples/shakespeare/hen_vi_2.xml'),
    ("Henry VI, Part 3",
        'http://www.ibiblio.org/xml/examples/shakespeare/hen_vi_3.xml'),
    ("The Life and Death of King John",
        'http://www.ibiblio.org/xml/examples/shakespeare/john.xml'),
    ("Julius Caesar",
        'http://www.ibiblio.org/xml/examples/shakespeare/j_caesar.xml'),
    ("King Lear",
        'http://www.ibiblio.org/xml/examples/shakespeare/lear.xml'),
    ("Love's Labor's Lost",
        'http://www.ibiblio.org/xml/examples/shakespeare/lll.xml'),
    ("Macbeth",
        'http://www.ibiblio.org/xml/examples/shakespeare/macbeth.xml'),
    ("The Merchant of Venice",
        'http://www.ibiblio.org/xml/examples/shakespeare/merchant.xml'),
    ("Much Ado About Nothing",
        'http://www.ibiblio.org/xml/examples/shakespeare/much_ado.xml'),
    ("Measure for Measure",
        'http://www.ibiblio.org/xml/examples/shakespeare/m_for_m.xml'),
    ("The Merry Wives of Windsor",
        'http://www.ibiblio.org/xml/examples/shakespeare/m_wives.xml'),
    ("Othello",
        'http://www.ibiblio.org/xml/examples/shakespeare/othello.xml'),
    ("Pericles",
        'http://www.ibiblio.org/xml/examples/shakespeare/pericles.xml'),
    ("Richard II",
        'http://www.ibiblio.org/xml/examples/shakespeare/rich_ii.xml'),
    ("Richard III",
        'http://www.ibiblio.org/xml/examples/shakespeare/rich_iii.xml'),
    ("Romeo and Juliet",
        'http://www.ibiblio.org/xml/examples/shakespeare/r_and_j.xml'),
    ("The Taming of the Shrew",
        'http://www.ibiblio.org/xml/examples/shakespeare/taming.xml'),
    ("The Tempest",
        'http://www.ibiblio.org/xml/examples/shakespeare/tempest.xml'),
    ("Timon of Athens",
        'http://www.ibiblio.org/xml/examples/shakespeare/timon.xml'),
    ("Titus Andronicus",
        'http://www.ibiblio.org/xml/examples/shakespeare/titus.xml'),
    ("Troilus and Cressida",
        'http://www.ibiblio.org/xml/examples/shakespeare/troilus.xml'),
    ("Two Gentlemen of Verona",
        'http://www.ibiblio.org/xml/examples/shakespeare/two_gent.xml'),
    ("Twelfth Night",
        'http://www.ibiblio.org/xml/examples/shakespeare/t_night.xml'),
    ("A Winter's Tale",
        'http://www.ibiblio.org/xml/examples/shakespeare/win_tale.xml'),
    ]
 
import shakespeare.gutenberg

class Helper(shakespeare.gutenberg.Helper):

    def __init__(self, verbose=False):
        self.verbose = verbose
        self._index = index

    def clean(self, line=None):
        raise Exception('Method not implemented')

    def add_to_db(self):
        """Add all texts to the db list of texts.
        
        If a text already exists in the db it will be skipped.
        """
        import shakespeare.dm
        for text in self._index:
            title = text[0]
            name = self.title_to_name(title) + '_moby'
            cachePath = shakespeare.utils.get_local_path(text[1])
            notes = 'Moby/Bosak Shakespeare, sourced from %s' % text[1]
            numExistingTexts = shakespeare.dm.Material.select(
                        shakespeare.dm.Material.q.name==name).count()
            if numExistingTexts > 0:
                if self.verbose:
                    print('Skip: Add to db. Moby/Bosak text already exists with name: %s' % name)
            else:
                if self.verbose:
                    print('Add to db. Moby/Bosak text named [%s]' % name)
                shakespeare.dm.Material(name=name,
                                        title=title,
                                        creator='Shakespeare, William',
                                        cache_path=cachePath,
                                        notes=notes)
