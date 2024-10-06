"""
https://wiki.python.org/moin/PyQt/Python%20syntax%20highlighting
"""


from PySide6 import QtGui
from PySide6.QtCore import QRegularExpression


def format(color, style=''):
    """
    Return a QTextCharFormat with the given attributes.
    """
    _format = QtGui.QTextCharFormat()
    _format.setForeground(color)
    if 'bold' in style:
        _format.setFontWeight(QtGui.QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


# Syntax styles that can be shared by all languages
STYLES = {
    'keyword': format(QtGui.QColor('#cc7832'), 'bold'),
    # 'operator': format('red'),
    # 'brace': format('darkGray'),
    'defclass': format(QtGui.QColor('#cc7832')),
    'string': format(QtGui.QColor(255, 255, 0)),
    'string2': format(QtGui.QColor('#829755'), 'italic'),
    'comment': format(QtGui.QColor('#47802c')),
    'self': format(QtGui.QColor('#94558d')),
    'numbers': format(QtGui.QColor('#6897bb')),
}


class PythonHighlighter(QtGui.QSyntaxHighlighter):
    """
    Syntax highlighter for the Python language.
    """
    # Python keywords
    keywords = [
        'and', 'assert', 'break', 'class', 'continue', 'def',
        'del', 'elif', 'else', 'except', 'exec', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in',
        'is', 'lambda', 'not', 'or', 'pass', 'print',
        'raise', 'return', 'try', 'while', 'yield',
        'None', 'True', 'False',
    ]

    # Python operators
    operators = [
        '=',
        # Comparison
        '==', '!=', '<', '<=', '>', '>=',
        # Arithmetic
        '\+', '-', '\*', '/', '//', '\%', '\*\*',
        # In-place
        '\+=', '-=', '\*=', '/=', '\%=',
        # Bitwise
        '\^', '\|', '\&', '\~', '>>', '<<',
    ]

    # Python braces
    braces = [
        '\{', '\}', '\(', '\)', '\[', '\]',
    ]

    def __init__(self, parent=None):
        super(PythonHighlighter, self).__init__(parent)

        # Multi-line strings (expression, flag, style)

        self.tri_single = (QRegularExpression("'''"), 1, STYLES['string2'])
        self.tri_double = (QRegularExpression('"""'), 2, STYLES['string2'])

        rules = []

        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
                  for w in PythonHighlighter.keywords]
        # rules += [(r'%s' % o, 0, STYLES['operator'])
        #           for o in PythonHighlighter.operators]
        # rules += [(r'%s' % b, 0, STYLES['brace'])
        #           for b in PythonHighlighter.braces]

        # All other rules
        rules += [
            # 'self'
            (r'\bself\b', 0, STYLES['self']),

            # 'def' followed by an identifier
            (r'\bdef\b\s*(\w+)', 1, STYLES['defclass']),
            # 'class' followed by an identifier
            (r'\bclass\b\s*(\w+)', 1, STYLES['defclass']),

            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),

            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),

            # From '#' until a newline
            (r'#[^\n]*', 0, STYLES['comment']),
        ]

        # Build a QRegExp for each pattern
        self.rules = [(QRegularExpression(pat), index, fmt)
                      for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        """
        Apply syntax highlighting to the given block of text.
        """
        self.tripleQuoutesWithinStrings = []
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            match = expression.match(text, 0)
            while match.hasMatch():
                index = match.capturedStart(nth)
                if index >= 0:
                    # if there is a string we check
                    # if there are some triple quotes within the string
                    # they will be ignored if they are matched again
                    if expression.pattern() in [r'"[^"\\]*(\\.[^"\\]*)*"', r"'[^'\\]*(\\.[^'\\]*)*'"]:
                        inner_match = self.tri_single[0].match(text, index + 1)
                        innerIndex = inner_match.capturedStart() if inner_match.hasMatch() else -1
                        if innerIndex == -1:
                            inner_match = self.tri_double[0].match(text, index + 1)
                            innerIndex = inner_match.capturedStart() if inner_match.hasMatch() else -1

                        if innerIndex != -1:
                            tripleQuoteIndexes = range(innerIndex, innerIndex + 3)
                            self.tripleQuoutesWithinStrings.extend(tripleQuoteIndexes)

                while index >= 0:
                    # skipping triple quotes within strings
                    if index in self.tripleQuoutesWithinStrings:
                        index += 1
                        match = expression.match(text, index)
                        if match.hasMatch():
                            index = match.capturedStart(nth)
                        continue

                    # We actually want the index of the nth match
                    length = match.capturedLength(nth)
                    self.setFormat(index, length, format)
                    match = expression.match(text, index + length)
                    if match.hasMatch():
                        index = match.capturedStart(nth)
                    else:
                        index = -1

        self.setCurrentBlockState(0)

        # Do multi-line strings
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)

    def match_multiline(self, text, delimiter, in_state, style):
        """
        Do highlighting of multi-line strings. ``delimiter`` should be a
        ``QRegularExpression`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            match = delimiter.match(text)
            start = match.capturedStart()

            # skipping triple quotes within strings
            if start in self.tripleQuoutesWithinStrings:
                return False
            # Move past this match
            add = match.capturedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            match = delimiter.match(text, start + add)
            end = match.capturedStart()

            # Look for the ending delimiter
            if end >= add:
                length = end - start + add + match.capturedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            match = delimiter.match(text, start + length)
            start = match.capturedStart() if match.hasMatch() else -1

        # Return True if still inside a multi-line string, False otherwise
        return self.currentBlockState() == in_state
