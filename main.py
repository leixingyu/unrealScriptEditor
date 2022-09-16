import ast
import os
import sys
import traceback
from importlib import reload
from collections import namedtuple

import unreal

from Qt import QtWidgets, QtCore, QtGui
from Qt import _loadUi

from .codeEditor import codeEditor
reload(codeEditor)
from .codeEditor.highlighter import pyHighlight
reload(pyHighlight)

from . import util

APP = None
WINDOW = None

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
MODULE_NAME = os.path.basename(MODULE_PATH)
UI_PATH = os.path.join(MODULE_PATH, 'ui', 'script_editor.ui')

CONFIG_PATH = os.path.join(MODULE_PATH, 'config.txt')

ERROR_FORMAT = QtGui.QTextCharFormat()
ERROR_FORMAT.setForeground(QtGui.QBrush(QtCore.Qt.red))

WARNING_FORMAT = QtGui.QTextCharFormat()
WARNING_FORMAT.setForeground(QtGui.QBrush(QtCore.Qt.yellow))

INFO_FORMAT = QtGui.QTextCharFormat()
INFO_FORMAT.setForeground(QtGui.QBrush(QtGui.QColor('#6897bb')))

REGULAR_FORMAT = QtGui.QTextCharFormat()
REGULAR_FORMAT.setForeground(QtGui.QBrush(QtGui.QColor(200, 200, 200)))


TabConfig = namedtuple('TabConfig', ['index', 'label', 'active', 'command'])


class ScriptEditorWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        """
        Initialization
        """
        super(ScriptEditorWindow, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.Window)
        _loadUi(UI_PATH, self)

        self.ui_tabs = list()
        self.ui_tab_highlighters = list()

        self.register_traceback()

        #
        self.load_configs()

        #
        self.ui_run_all_btn.setIcon(QtGui.QIcon(":/executeAll.png"))
        self.ui_run_sel_btn.setIcon(QtGui.QIcon(":/execute.png"))
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

        self.ui_tab_widget.tabBarClicked.connect(self.add_tab)
        self.ui_tab_widget.tabCloseRequested.connect(self.close_tab)

    # Initialize

    def closeEvent(self, event):
        self.save_configs()
        super(ScriptEditorWindow, self).closeEvent(event)

    def register_traceback(self):
        def custom_traceback(exc_type, exc_value, exc_traceback=None):
            message = 'Error: {}: {}\n'.format(exc_type, exc_value)
            if exc_traceback:
                format_exception = traceback.format_tb(exc_traceback)
                for line in format_exception:
                    message += line
            self.update_logger(message, 'error')

        sys.excepthook = custom_traceback

    # Config

    def save_configs(self):
        configs = list()
        active_index = self.ui_tab_widget.currentIndex()

        for i in range(self.ui_tab_widget.count()-1):
            self.ui_tab_widget.setCurrentIndex(i)
            script_tab = self.ui_tab_widget.currentWidget()
            label = self.ui_tab_widget.tabText(i)
            active = active_index == i

            config = TabConfig(i, label, active, script_tab.toPlainText())
            configs.append(config)

        # go back to the previous active tab
        self.ui_tab_widget.setCurrentIndex(active_index)

        with open(CONFIG_PATH, 'w') as f:
            string = [config._asdict() for config in configs]
            f.write(str(string))

    def load_configs(self):
        if not os.path.exists(CONFIG_PATH):
            self.load_tabs()
            return

        with open(CONFIG_PATH, 'r') as f:
            tab_configs = list()
            tab_config_dicts = ast.literal_eval(f.read())
            for tab_config_dict in tab_config_dicts:
                tab_config = TabConfig(**tab_config_dict)
                tab_configs.append(tab_config)

        self.load_tabs(tab_configs)

    def load_tabs(self, tab_configs=None):
        if not tab_configs:
            tab_configs = [TabConfig(0, 'Python', True, '')]

        active_index = 0
        for tab_config in tab_configs:
            self.insert_tab(tab_config.index, tab_config.command, tab_config.label)
            if tab_config.active:
                active_index = tab_config.index

        self.ui_tab_widget.setCurrentIndex(active_index)

    def insert_tab(self, index, command, label):
        script_edit = codeEditor.CodeEditor()
        script_edit.setPlainText(command)
        highlight = pyHighlight.PythonHighlighter(
            script_edit.document())

        self.ui_tab_widget.insertTab(index, script_edit, label)
        self.ui_tab_highlighters.append(highlight)
        self.ui_tabs.append(script_edit)

        self.ui_tab_widget.setCurrentIndex(index)

    # Execution

    def execute(self):
        """
        Send all command in script area for maya to execute
        """
        command = self.ui_tab_widget.currentWidget().toPlainText()
        output = util.execute_python_command(command)

        if not output:
            return

        self.update_logger('# Script executed:')
        self.update_logger(command)
        self.update_logger('# Script execution ended')
        self.send_formatted_output(output)

    def execute_sel(self):
        """
        Send selected command in script area for maya to execute
        """
        command = self.ui_tab_widget.currentWidget().textCursor().selection().toPlainText()
        output = util.execute_python_command(command)

        if not output:
            return

        self.update_logger('# Command executed:')
        self.update_logger(command)
        self.update_logger('# Command execution ended')
        self.send_formatted_output(output)

    def send_formatted_output(self, output):
        """
        Update ui field with messages
        """
        if not output:
            return

        result, log_entries = output
        for entry in log_entries:
            if entry.type != unreal.PythonLogOutputType.INFO:
                self.update_logger(entry.output, 'error')
            else:
                self.update_logger(entry.output, 'info')

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

    def clear_log(self):
        """
        Clear history logging area
        """
        self.ui_log_edit.clear()

    def clear_script(self):
        self.ui_tab_widget.currentWidget().setPlainText('')

    def clear_all(self):
        self.clear_script()
        self.clear_log()

    # Tab Operation

    def add_tab(self, index):
        # add tab clicked
        if index == self.ui_tab_widget.count() - 1:
            self.insert_tab(index, '', 'Python')

    def close_tab(self, index):
        if index != self.ui_tab_widget.count() - 1:
            self.ui_tab_widget.removeTab(index)
            self.ui_tab_widget.setCurrentIndex(index-1)

    # IO

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
            file_name = os.path.basename(path)
            output = f.read()
            index = self.ui_tab_widget.count() - 1
            self.insert_tab(index, output, file_name)

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

        command = self.ui_tab_widget.currentWidget().toPlainText()
        with open(path, 'w') as f:
            f.write(command)


def show():
    global APP
    global WINDOW

    if not QtWidgets.QApplication.instance():
        APP = QtWidgets.QApplication(sys.argv)

    QtCore.QResource.registerResource(
        os.path.join(MODULE_PATH, "icons", "icons.rcc"))

    # stylesheet
    QtCore.QResource.registerResource(
        os.path.join(MODULE_PATH, "stylesheet", "icons.rcc"))
    with open(os.path.join(MODULE_PATH, "stylesheet", "ue.qss"), 'r') as f:
        qss = f.read()
        APP.setStyleSheet(qss)

    exists = WINDOW is not None

    if not exists:
        WINDOW = ScriptEditorWindow()
        unreal.parent_external_window_to_slate(
            WINDOW.winId().__init__(),
            unreal.SlateParentWindowSearchMethod.ACTIVE_WINDOW
        )

    WINDOW.showNormal()
    unreal.log_warning("Does {} have parent: {}".format(WINDOW.winId(), WINDOW.parent()))
    return WINDOW
