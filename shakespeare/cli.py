#!/usr/bin/env python

import cmd
import os
import StringIO

class ShakespeareAdmin(cmd.Cmd):
    """
    TODO: self.verbose option and associated self._print
    """

    def __init__(self, verbose=False):
        # cmd.Cmd is not a new style class
        cmd.Cmd.__init__(self)
        self.verbose = verbose

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

For more information about the package run `info`.
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
            print 'To create db use paster: paster setup-app {config-file}'

    def help_db(self, line=None):
        usage = \
'''db { create | init }
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

    def do_runserver(self, line=None):
        self.help_runserver()

    def help_runserver(self, line=None):
        usage = \
'''This command has been DEPRECATED.

Please use `paster serve` to run a server now, e.g.::

    paster serve <my-config.ini>
'''
        print usage
    
    def do_info(self, line=None):
        import shakespeare
        info = shakespeare.__doc__
        print
        print '       ## Open Shakespeare ##'
        print info
    
    def help_info(self, line=None):
        print 'Information about this package.'

    def _parse_line(self, line):
        line = line.strip()
        args = line.split()
        action = ''
        remainder = ''
        if len(args) > 0:
            action = args[0]
        if len(args) > 1:
            remainder = ' '.join(args[1:])
        return (action, remainder)

    def do_search(self, line):
        import shakespeare.search
        index = shakespeare.search.SearchIndex.default_index()

        action, extra = self._parse_line(line)
        if action == 'addpath':
            index.add_from_path(extra)
        elif action == 'query':
            results = index.search(extra)
            print index.print_matches(results)
        elif action == 'addtext':
            import shakespeare.model as model
            text = model.Material.byName(extra)
            fileobj = text.get_text()
            index.add_item(fileobj)
        elif action == 'init':
            self._init_index()
            for text in self._index:
                fileobj = text.get_text()
                index.add_item(fileobj)
        else:
            print 'Unrecognized action: %s' % action
            self.help_search()
            return 1

    def help_search(self, line=None):
        info = \
'''
search addpath {path}
    - Add contents of {path} (file itself or all text files in directory if
      directory) to the search index.
      
search addtext {name}
    - Add db text named {name} to search index.

search query {query}
    - Query search index with {query}.

search init
    - Add all texts in DB to index.
'''
        print info

    def do_stats(self, line):
        action, extra = self._parse_line(line)

        import shakespeare.stats
        stats = shakespeare.stats.Stats()
        if action == 'init':
            self._init_index()
            for text in self._index:
                stats.statsify(text, text.get_text())
        elif action == 'addtext':
            import shakespeare.model as model
            text = model.Material.byName(extra)
            stats.statsify(text, text.get_text())
        elif action == 'show':
            textstats = stats.text_stats(extra)
            for s in textstats:
                print s.word, s.freq
        else:
            print 'Unrecognized action: %s' % action
            self.help_stats()
            return 1

    def help_stats(self, line=None):
        info = \
'''
stats addtext {name}
    - Add db text named {name} to stats index.

stats show {name}
    - Query stats index with {query}.

stats init
    - Prepare statistics for all texts in DB.
'''
        print info


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
        cmd = ShakespeareAdmin(verbose=options.verbose)
        args = ' '.join(args)
        args = args.replace('-','_')
        cmd.onecmd(args)

