"""
code for the main script editor window
"""

import ast
import os
import sys
import traceback
from collections import namedtuple

try:
    import unreal
    RUNNING_IN_UNREAL = True
except ImportError:
    RUNNING_IN_UNREAL = False

from Qt import QtWidgets, QtCore, QtGui
from Qt import _loadUi

from . import outputTextWidget
from .codeEditor import codeEditor
from .codeEditor.highlighter import pyHighlight

APP = None
WINDOW = None

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
MODULE_NAME = os.path.basename(MODULE_PATH)
UI_PATH = os.path.join(MODULE_PATH, 'ui', 'script_editor.ui')
CONFIG_PATH = os.path.join(MODULE_PATH, 'config.txt')

ICONS_PATH = os.path.join(MODULE_PATH, 'icons')
QtCore.QDir.addSearchPath("ICONS", ICONS_PATH)


class TabConfig(namedtuple('TabConfig', ['index', 'label', 'active', 'command'])):
    """
    Dataclass to store python script information in the tabs

    :param index: int. script tab index within the tab widget
    :param label: str. script tab title label
    :param active: bool. whether this tab is set to active (current)
                   only one tab is allowed to be active
    :param command: str. script in the tab
    """
    __slots__ = ()


class ScriptEditorWindow(QtWidgets.QMainWindow):
    """
    Script Editor main window
    """

    def __init__(self, parent=None):
        """
        Initialization
        """
        super(ScriptEditorWindow, self).__init__(parent)
        _loadUi(UI_PATH, self)
        splitter = QtWidgets.QSplitter()
        splitter.setOrientation(QtCore.Qt.Vertical)
        self.centralwidget.layout().addWidget(splitter)
        self.ui_log_edit = outputTextWidget.OutputTextWidget()
        splitter.addWidget(self.ui_log_edit)
        splitter.addWidget(self.ui_tab_widget)

        self.ui_tabs = list()
        self.ui_tab_highlighters = list()

        self.register_traceback()
        self.load_configs()

        #
        self.ui_run_all_btn.clicked.connect(self.execute)
        self.ui_run_sel_btn.clicked.connect(self.execute_sel)
        self.ui_clear_log_btn.clicked.connect(self.clear_log)
        self.ui_clear_script_btn.clicked.connect(self.clear_script)
        self.ui_clear_both_btn.clicked.connect(self.clear_all)

        self.ui_save_action.triggered.connect(self.save_script)
        self.ui_open_action.triggered.connect(self.open_script)

        self.ui_tab_widget.tabBarClicked.connect(self.add_tab)
        self.ui_tab_widget.tabCloseRequested.connect(self.remove_tab)

    # region Overrides
    def closeEvent(self, event):
        """
        Override: close the tool automatically saves out the script configs
        """
        self.save_configs()
        super(ScriptEditorWindow, self).closeEvent(event)

    def register_traceback(self):
        """
        Link Unreal traceback
        """
        def custom_traceback(exc_type, exc_value, exc_traceback=None):
            message = 'Error: {}: {}\n'.format(exc_type, exc_value)
            if exc_traceback:
                format_exception = traceback.format_tb(exc_traceback)
                for line in format_exception:
                    message += line
            self.ui_log_edit.update_logger(message, 'error')

        sys.excepthook = custom_traceback
    # endregion

    # region Config
    def save_configs(self):
        """
        Save all current python tabs' config
        """
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
        """
        During startup, load python script config file and initialize tab gui
        """
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
        """
        Initialize python script tab gui from config object

        :param tab_configs: TabConfig. dataclass object storing python tab info
        """
        if not tab_configs:
            tab_configs = [TabConfig(0, 'Python', True, '')]

        active_index = 0
        for tab_config in tab_configs:
            self.insert_tab(tab_config.index, tab_config.command, tab_config.label)
            if tab_config.active:
                active_index = tab_config.index

        self.ui_tab_widget.setCurrentIndex(active_index)

    def insert_tab(self, index, command, label):
        """
        Insert a python tab into the tab widget

        :param index: int. tab index to insert
        :param command: str. python script command to add to the inserted tab
        :param label: str. title/label of the tab inserted
        """
        script_edit = codeEditor.CodeEditor()
        script_edit.setPlainText(command)
        highlight = pyHighlight.PythonHighlighter(
            script_edit.document())

        self.ui_tab_widget.insertTab(index, script_edit, label)
        self.ui_tab_highlighters.append(highlight)
        self.ui_tabs.append(script_edit)

        self.ui_tab_widget.setCurrentIndex(index)
    # endregion

    # region Execution
    def execute(self):
        """
        Send all command in script area for maya to execute
        """
        command = self.ui_tab_widget.currentWidget().toPlainText()
        if RUNNING_IN_UNREAL:
            output = unreal.PythonScriptLibrary.execute_python_command_ex(
                python_command=command,
                execution_mode=unreal.PythonCommandExecutionMode.EXECUTE_FILE,
                file_execution_scope=unreal.PythonFileExecutionScope.PUBLIC
            )

            if not output:
                return

            self.ui_log_edit.update_logger(
                "# Command executed: \n"
                "{}\n"
                "# Command execution ended".format(command)
            )
            self.send_formatted_output(output)
        else:
            # todo this wont get any output, fix it
            output = None
            exec(command)

    def execute_sel(self):
        """
        Send selected command in script area for maya to execute
        """
        command = self.ui_tab_widget.currentWidget().textCursor().selection().toPlainText()
        if RUNNING_IN_UNREAL:
            output = unreal.PythonScriptLibrary.execute_python_command_ex(
                python_command=command,
                execution_mode=unreal.PythonCommandExecutionMode.EXECUTE_FILE,
                file_execution_scope=unreal.PythonFileExecutionScope.PUBLIC
            )

            if not output:
                return

            self.ui_log_edit.update_logger(
                "# Command executed: \n"
                "{}\n"
                "# Command execution ended".format(command)
            )
            self.send_formatted_output(output)
        else:
            # todo this wont get any output, fix it
            output = None
            exec(command)

    def send_formatted_output(self, output):
        """
        Update ui field with messages
        """
        if not output:
            return

        result, log_entries = output
        for entry in log_entries:
            if entry.type != unreal.PythonLogOutputType.INFO:
                self.ui_log_edit.update_logger(entry.output, 'error')
            else:
                self.ui_log_edit.update_logger(entry.output, 'info')

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
    # endregion

    # region Tab Operation
    def add_tab(self, index):
        """
        Add a python tab when 'Add' tab button is clicked
        """
        if index == self.ui_tab_widget.count() - 1:
            self.insert_tab(index, '', 'Python')

    def remove_tab(self, index):
        """
        Remove a python tab

        :param index: int. removal tab index
        """
        msg_box = QtWidgets.QMessageBox(
            QtWidgets.QMessageBox.Question,
            '',
            'Delete the Current Tab?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )

        usr_choice = msg_box.exec()
        if usr_choice == QtWidgets.QMessageBox.Yes:
            if index != self.ui_tab_widget.count() - 1:
                self.ui_tab_widget.removeTab(index)
                self.ui_tab_widget.setCurrentIndex(index-1)
    # endregion

    # region File IO
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
    # endregion


def show():
    global APP
    global WINDOW

    APP = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    # stylesheet
    QtCore.QResource.registerResource(
        os.path.join(MODULE_PATH, "stylesheet", "icons.rcc"))
    with open(os.path.join(MODULE_PATH, "stylesheet", "ue.qss"), 'r') as f:
        qss = f.read()
        APP.setStyleSheet(qss)

    # handles existing instance
    exists = WINDOW is not None
    if not exists:
        WINDOW = ScriptEditorWindow()
    WINDOW.show()

    if RUNNING_IN_UNREAL:
        unreal.parent_external_window_to_slate(int(WINDOW.winId()))

    return WINDOW
