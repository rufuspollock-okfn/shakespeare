#!/usr/bin/env python

import cmd
import os
import StringIO

class ShakespeareAdmin(cmd.Cmd):
    """
    TODO: self.verbose option and associated self._print
    """

    def __init__(self, config=None, verbose=False):
        # cmd.Cmd is not a new style class
        cmd.Cmd.__init__(self)
        self.config = config
        self.verbose = verbose

    def _print(self, msg, force=False):
        if self.verbose or force:
            print msg

    def _register_config(self):
        import sys
        if not self.config:
            msg = 'No configuration file has been specified. See -h help for details'
            print msg
            sys.exit(1)
        import shakespeare
        shakespeare.register_config(self.config)

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
        actions = [ 'create', 'clean', 'init' ]
        if line is None or line not in actions:
            self.help_db()
            return 1
        self._register_config()
        import shakespeare.model as model
        import shakespeare
        if line == 'init':
            model.metadata.create_all()
            import shksprdata.load
            shksprdata.load.load_texts()
        elif line == 'clean':
            config = shakespeare.conf()
            model.metadata.drop_all()
        elif line == 'create':
            model.metadata.create_all()
        else:
            print self.help_db()

    def help_db(self, line=None):
        usage = \
'''db { create | init | clean }
'''
        print usage
    
    def _init_index(self):
        self._register_config()
        import shakespeare.model as model
        self._index = model.Material.query.all()

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
'''Print index of texts to stdout'''
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
        self._register_config()
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
            index.add_item(fileobj, text.name)
        elif action == 'init':
            self._init_index()
            for text in self._index:
                # exclude folios as many odd spellings
                if text.name.endswith('_f'):
                    continue
                self._print('Adding: %s' % text.name)
                fileobj = text.get_text()
                index.add_item(fileobj, text.name)
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
        self._register_config()
        action, extra = self._parse_line(line)

        import shakespeare.stats
        stats = shakespeare.stats.Stats()
        if action == 'init':
            self._init_index()
            for text in self._index:
                # exclude folios as many odd spellings
                if text.name.endswith('_f'):
                    continue
                self._print('Adding: %s' % text.name)
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

For list of the commands available run:

    $ shakespeare-admin help

For more general information run the about or info commands.'''
    parser = optparse.OptionParser(usage)
    parser.add_option('-v', '--verbose', dest='verbose', help='Be verbose',
            action='store_true', default=False) 
    parser.add_option('-c', '--config', dest='config',
        help='Path to config file', default=None)
    options, args = parser.parse_args()
    
    if len(args) == 0:
        parser.print_help()
        return 1
    else:
        cmd = ShakespeareAdmin(verbose=options.verbose, config=options.config)
        args = ' '.join(args)
        args = args.replace('-','_')
        cmd.onecmd(args)

