class TextFormatter(object):
    """Format a provided text in a variety of ways.
    For example: add line numbers, convert to html with line ids etc
    """

    def __init__(self, file):
        """
        @file: file-like object containing a text in plain txt
        """
        self.file = file

    def format(self, format):
        """
        @format: the name specifying the format to use
        """
        if format == 'lineno':
            return self.add_line_numbers()
        else:
            raise ValueError('Unknown format: %s' % format)
    
    def add_line_numbers(self):
        result = ''
        count = 0
        for line in self.file.readlines():
            tlineno = str(count).ljust(4) # assume line no < 10000
            result += '<pre id="%s">%s %s</pre>\n' % (count, tlineno, line.rstrip())
            count += 1
        return result
