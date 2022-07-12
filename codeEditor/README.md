<div align="center">
<h1 align="center">Qt Code Editor</h1>

  <p align="center">
    A PyQt5/PySide2 version of code editor with line counter and syntax highlighting
  </p>
</div>

## About The Project

<br>

<div align="left">
<img src="https://i.imgur.com/slpRvWD.png" alt="code-editor" width="70%"/>
</div>

<br>

A central repo to store useful stuff related to creating a code editor based on PyQt.
It currently consists of the main code editor subclassing from `QPlainTextEdit` with
a side widget for line counter. It currently supports syntax highlighting for
`.json` and `.py` files, they are `QSyntaxHighlighter` class which can be found
in the **highlighter** folder.

## Getting Started

### Prerequisites

- [Qt](https://github.com/mottosso/Qt.py): a module that supports different
python qt bindings

   or alternatively, change the code below to whatever qt binding you have on your machine.
   ```python
   from Qt import QtWidgets, QtCore, QtGui
   from Qt import _loadUi
   ```

### Launch

1. Unzip the **qt-code-editor** package and run `main.py` directly

2. Or include the following snippet to your ui code to create a
code editor with syntax highlighting.
    ```python
    import codeEditor
    from highlighter.pyHighlight import PythonHighlighter

    editor = codeEditor.CodeEditor()
    highlighter = PythonHighlighter(editor.document())
    ```

### Reference

[Qt Documentation - Code Editor Example](https://doc.qt.io/qt-5/qtwidgets-widgets-codeeditor-example.html)

[Qt for Python 6.2.2 - Code Editor Example](https://doc.qt.io/qtforpython/examples/example_widgets__codeeditor.html)

[Python.org - Python syntax highlighting](https://wiki.python.org/moin/PyQt/Python%20syntax%20highlighting)

