"""
Module for setting up the listen server which sends command to
Maya's command port, and also actively listens to Maya's return message
from callback.

Requirement:
needs Maya to open a command port first, run it before connecting or
put it in the setup file for startup.

import maya.cmds as cmds
if not cmds.commandPort(":5050", query=True):
    cmds.commandPort(name=":5050")
"""


import os
import sys
import traceback
from importlib import reload

import unreal

from Qt import QtWidgets, QtCore, QtGui
from Qt import _loadUi

from .codeEditor import codeEditor
from .codeEditor.highlighter import pyHighlight

from . import util


MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
MODULE_NAME = os.path.basename(MODULE_PATH)
UI_PATH = os.path.join(MODULE_PATH, 'ui', 'connector.ui')


class ScriptEditorWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        """
        Initialization
        """
        super(ScriptEditorWindow, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        _loadUi(UI_PATH, self)

        self.register_traceback()

        #
        self.ui_script_edit = codeEditor.CodeEditor()
        self.ui_python_layout.addWidget(self.ui_script_edit)
        self.highlight = pyHighlight.PythonHighlighter(self.ui_script_edit.document())

        self.load_configs()

        #
        self.ui_run_all_btn.setIcon(QtGui.QIcon(":/executeAll.png"))
        self.ui_run_sel_btn.setIcon(QtGui.QIcon(":/execute.png"))
        self.ui_connect_btn.setIcon(QtGui.QIcon(":/connect.png"))
        self.ui_disconnect_btn.setIcon(QtGui.QIcon(":/disconnect.png"))
        self.ui_clear_log_btn.setIcon(QtGui.QIcon(":/clearHistory.png"))
        self.ui_clear_script_btn.setIcon(QtGui.QIcon(":/clearInput.png"))
        self.ui_clear_both_btn.setIcon(QtGui.QIcon(":/clearAll.png"))
        #
        self.ui_run_all_btn.clicked.connect(self.execute)
        self.ui_run_sel_btn.clicked.connect(self.execute_sel)
        self.ui_clear_log_btn.clicked.connect(self.clear_log)
        self.ui_clear_script_btn.clicked.connect(self.clear_script)
        self.ui_clear_both_btn.clicked.connect(self.clear_all)
        self.ui_save_action.triggered.connect(self.save_script)
        self.ui_open_action.triggered.connect(self.open_script)

    def closeEvent(self, event):
        self.save_configs()

        self.setHidden(True)

        # super(ScriptEditorWindow, self).closeEvent(event)

    def save_configs(self):
        pass

    def load_configs(self):
        pass

    def register_traceback(self):
        def custom_traceback(exc_type, exc_value, exc_traceback=None):
            self.update_logger('Type: {}; Value: {};'.format(exc_type, exc_value))

            if exc_traceback:
                format_exception = traceback.format_tb(exc_traceback)
                for line in format_exception:
                    self.update_logger(repr(line))

        sys.excepthook = custom_traceback

    def execute(self):
        """
        Send all command in script area for maya to execute
        """
        command = self.ui_script_edit.toPlainText()
        output = util.execute_python_command(command)
        self.send_output(output)

    def execute_sel(self):
        """
        Send selected command in script area for maya to execute
        """
        command = self.ui_script_edit.textCursor().selection().toPlainText()
        output = util.execute_python_command(command)
        self.send_output(output)

    def send_output(self, output):
        """
        Update ui field with messages
        """
        if not output:
            return

        result, log_entries = output
        unreal.log(result)

        for entry in log_entries:
            line = ('{}:{}'.format(
                entry.type,
                entry.output
            ))
            self.update_logger(line)

    def update_logger(self, message):
        self.ui_log_edit.insertPlainText(message)
        self.ui_log_edit.insertPlainText('\n')

        scroll = self.ui_log_edit.verticalScrollBar()
        scroll.setValue(scroll.maximum())

    def clear_script(self):
        """
        Clear script edit area
        """
        self.ui_script_edit.clear()

    def clear_log(self):
        """
        Clear history logging area
        """
        self.ui_log_edit.clear()

    def clear_all(self):
        """
        Clear both script edit area and history logging area
        """
        self.clear_log()
        self.clear_script()

    def open_script(self):
        """
        Open python file to script edit area
        """
        path = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "Open Script",
            MODULE_PATH,
            filter="*.py")[0]

        if not path:
            return

        with open(path, 'r') as f:
            output = f.read()
            self.ui_script_edit.setPlainText(output)

    def save_script(self):
        """
        Save script edit area as a python file
        """
        path = QtWidgets.QFileDialog.getSaveFileName(
            None,
            "Save Script As...",
            MODULE_PATH,
            filter="*.py")[0]

        if not path:
            return

        command = self.ui_script_edit.toPlainText()
        with open(path, 'w') as f:
            f.write(command)


window = None


def show():
    global app
    global window

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)

    QtCore.QResource.registerResource(
        os.path.join(MODULE_PATH, "icons", "icons.rcc"))

    # stylesheet
    # QtCore.QResource.registerResource(
    #     os.path.join(MODULE_PATH, "stylesheet", "icons.rcc"))
    # with open(os.path.join(MODULE_PATH, "stylesheet", "ue.qss"), 'r') as f:
    #     qss = f.read()
    #     app.setStyleSheet(qss)

    exists = window is not None

    if not exists:
        unreal.log('created new instance')
        window = ScriptEditorWindow()
        unreal.parent_external_window_to_slate(
            window.winId().__init__(),
            unreal.SlateParentWindowSearchMethod.ACTIVE_WINDOW
        )
    window.showNormal()

    return window

