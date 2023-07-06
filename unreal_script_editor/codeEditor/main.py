import sys

from Qt import QtWidgets

import codeEditor
from highlighter.pyHighlight import PythonHighlighter


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    editor = codeEditor.CodeEditor()
    editor.setWindowTitle("Code Editor Example")
    highlighter = PythonHighlighter(editor.document())
    editor.show()

    sys.exit(app.exec_())
