#!/usr/bin/env python

import cmd
import os
import StringIO

class ShakespeareAdmin(cmd.Cmd):
    """
    TODO: self.verbose option and associated self._print
    """

    prompt = 'The Bard > '

    def run_interactive(self, line=None):
        """Run an interactive session.
        """
        print 'Welcome to shakespeare-admin interactive mode\n'
        self.do_about()
        print 'Type:  "?" or "help" for help on commands.\n'
        while 1:
            try:
                self.cmdloop()
                break
            except KeyboardInterrupt:
                raise

    def do_help(self, line=None):
        cmd.Cmd.do_help(self, line)

    def do_about(self, line=None):
        import shakespeare
        version = shakespeare.__version__
        about = \
'''Open Shakespeare version %s. Copyright the Open Knowledge Foundation.
Open Shakespeare is open-knowledge and open-source. See COPYING for details.
''' % version
        print about

    def do_quit(self, line=None):
        sys.exit()

    def do_EOF(self, *args):
        print ''
        sys.exit()

    # =================
    # Commands

    def do_db(self, line=None):
        actions = [ 'create', 'clean', 'rebuild', 'init' ]
        if line is None or line not in actions:
            self.help_db()
            return 1
        import shakespeare.model
        if line == 'init':
            import pkg_resources
            pkg = 'shksprdata'
            meta = pkg_resources.resource_stream(pkg, 'texts/metadata.txt')
            shakespeare.model.Material.load_from_metadata(meta)
        else:
            shakespeare.model.__dict__[line+'db']()

    def help_db(self, line=None):
        usage = \
'''db { create | clean | rebuild | init }
'''
        print usage
    
    def do_gutenberg(self, line=None):
        import shakespeare.gutenberg
        helper = shakespeare.gutenberg.Helper(verbose=True)
        if not line:
            helper.execute()
        elif line == 'print_index':
            import pprint
            pprint.pprint(helper.get_index())
        else:
            msg = 'Unknown argument %s' % line
            raise Exception(msg)

    def help_gutenberg(self, line=None):
        usage = \
"""
Download and process all Project Gutenberg shakespeare texts"""
        print usage 

    def do_moby(self, line=None):
        import shakespeare.moby
        helper = shakespeare.moby.Helper(verbose=True)
        if not line:
            helper.execute()
        elif line == 'print_index':
            import pprint
            pprint.pprint(helper.get_index())
        else:
            msg = 'Unknown argument %s' % line
            raise Exception(msg)

    def help_moby(self, line=None):
        usage = \
'''
Download and process all Moby/Bosak shakespeare texts'''
        print usage 

    def _init_index(self):
        import shakespeare.index
        self._index = shakespeare.index.all

    def _filter_index(self, line):
        """Filter items in index return only those whose id (url) is in line
        If line is empty or None return all items
        """
        if line:
            textsToAdd = []
            textNames = line.split()
            for item in self._index:
                if item.name in textNames:
                    textsToAdd.append(item)
            return textsToAdd
        else:
            self._init_index()
            return self._index
    
    def do_index(self, line):
        self._init_index()
        header = \
'''          +-------------------+
          | Index of Material |
          +-------------------+

'''
        print header
        for row in self._index:
            print row.name.ljust(35), row.title

    def help_index(self, line=None):
        usage = \
'''Print index of Shakespeare texts to stdout'''
        print usage

    def do_concordance(self, line=None):
        self._init_index()
        print 'Making concordance (this may take some time ...):'
        from shakespeare.concordance import ConcordanceBuilder
        import time
        start = end = 0
        start = time.time()
        cc = ConcordanceBuilder()
        textsToAdd = []
        if line is not None:
            textsToAdd = self._filter_index(line)
        else:
            def gut_non_folio(material):
                return '_gut' in material.name and 'gut_f' not in material.name
            textsToAdd = filter(gut_non_folio, self._index) 
        for item in textsToAdd:
            print 'Adding: %s (%s)' % (item.name, item.title)
            cc.add_text(item.name)
        end = time.time()
        timetaken = end - start
        print 'Finished. Time taken was %ss' % timetaken

    def help_concordance(self, line=None):
        usage = \
'''Create a concordance

If no arguments supplied then use all non-folio gutenberg shakespeare texts.
Otherwise arguments should be a space seperated list of work name ids
'''
        print usage

    def do_runserver(self, line=None):
        self.help_runserver()

    def help_runserver(self, line=None):
        usage = \
'''This command has been DEPRECATED.

Please use `paster serve` to run a server now, e.g.::

    paster serve <my-config.ini>
'''
        print usage


def main():
    import optparse
    usage = \
'''%prog [options] <command>

Run about or help for details.'''
    parser = optparse.OptionParser(usage)
    parser.add_option('-v', '--verbose', dest='verbose', help='Be verbose',
            action='store_true', default=False) 
    options, args = parser.parse_args()
    
    if len(args) == 0:
        parser.print_help()
        return 1
    else:
        cmd = ShakespeareAdmin()
        args = ' '.join(args)
        args = args.replace('-','_')
        cmd.onecmd(args)

