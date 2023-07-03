from Qt import QtWidgets, QtCore, QtGui


class HighlightRule(object):
    def __init__(self, pattern, cformat):
        self.pattern = pattern
        self.format = cformat


class JsonHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent=None):
        """
        Initialize rules with expression pattern and text format
        """
        super(JsonHighlighter, self).__init__(parent)

        self.rules = list()

        # cformat = QtGui.QTextCharFormat()
        # cformat.setForeground(QtCore.Qt.darkMagenta)
        # cformat.setFontWeight(QtGui.QFont.Bold)

        # for pattern in [r"\{", r"\}", r"\[", r"\]"]:
        #     rule = HighlightRule()
        #     rule.pattern = QtCore.QRegExp(pattern)
        #     rule.format = cformat
        #     self.rules.append(rule)

        # numeric value
        cformat = QtGui.QTextCharFormat()
        cformat.setForeground(QtCore.Qt.darkBlue)
        cformat.setFontWeight(QtGui.QFont.Bold)
        pattern = QtCore.QRegExp("([-0-9.]+)(?!([^\"]*\"[\\s]*\\:))")

        rule = HighlightRule(pattern, cformat)
        self.rules.append(rule)

        # key
        cformat = QtGui.QTextCharFormat()
        pattern = QtCore.QRegExp("(\"[^\"]*\")\\s*\\:")
        # cformat.setForeground(QtCore.Qt.darkMagenta)
        cformat.setFontWeight(QtGui.QFont.Bold)

        rule = HighlightRule(pattern, cformat)
        self.rules.append(rule)

        # value
        cformat = QtGui.QTextCharFormat()
        pattern = QtCore.QRegExp(":+(?:[: []*)(\"[^\"]*\")")
        cformat.setForeground(QtCore.Qt.darkGreen)

        rule = HighlightRule(pattern, cformat)
        self.rules.append(rule)

    def highlightBlock(self, text):
        """
        Override: implementing virtual method of highlighting the text block
        """
        for rule in self.rules:
            # create a regular expression from the retrieved pattern
            expression = QtCore.QRegExp(rule.pattern)

            # check what index that expression occurs at with the ENTIRE text
            index = expression.indexIn(text)
            while index >= 0:
                # get the length of how long the expression is
                # set format from the start to the length with the text format
                length = expression.matchedLength()
                self.setFormat(index, length, rule.format)

                # set index to where the expression ends in the text
                index = expression.indexIn(text, index + length)
