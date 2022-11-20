import os

from Qt import QtWidgets, QtCore, QtGui
from Qt import _loadUi


MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
MODULE_NAME = os.path.basename(MODULE_PATH)
UI_PATH = os.path.join(MODULE_PATH, 'ui', 'output_text_widget.ui')


ERROR_FORMAT = QtGui.QTextCharFormat()
ERROR_FORMAT.setForeground(QtGui.QBrush(QtCore.Qt.red))

WARNING_FORMAT = QtGui.QTextCharFormat()
WARNING_FORMAT.setForeground(QtGui.QBrush(QtCore.Qt.yellow))

INFO_FORMAT = QtGui.QTextCharFormat()
INFO_FORMAT.setForeground(QtGui.QBrush(QtGui.QColor('#6897bb')))

REGULAR_FORMAT = QtGui.QTextCharFormat()
REGULAR_FORMAT.setForeground(QtGui.QBrush(QtGui.QColor(200, 200, 200)))


class OutputTextWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        """
        Initialization
        """
        super(OutputTextWidget, self).__init__(parent)
        _loadUi(UI_PATH, self)

    def clear(self):
        self.ui_log_edit.clear()

    def update_logger(self, message, mtype=None):
        if mtype == 'info':
            self.ui_log_edit.setCurrentCharFormat(INFO_FORMAT)
        elif mtype == 'warning':
            self.ui_log_edit.setCurrentCharFormat(WARNING_FORMAT)
        elif mtype == 'error':
            self.ui_log_edit.setCurrentCharFormat(ERROR_FORMAT)
        else:
            self.ui_log_edit.setCurrentCharFormat(REGULAR_FORMAT)

        self.ui_log_edit.insertPlainText(message)
        self.ui_log_edit.insertPlainText('\n')

        scroll = self.ui_log_edit.verticalScrollBar()
        scroll.setValue(scroll.maximum())

    def update_logger_html(self, html):
        self.ui_log_edit.insertHtml(html)
        self.ui_log_edit.insertHtml('<br>')

        scroll = self.ui_log_edit.verticalScrollBar()
        scroll.setValue(scroll.maximum())
