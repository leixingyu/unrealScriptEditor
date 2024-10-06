# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'script_editor.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QHBoxLayout,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(567, 569)
        self.ui_save_action = QAction(MainWindow)
        self.ui_save_action.setObjectName(u"ui_save_action")
        font = QFont()
        font.setFamilies([u"Bahnschrift"])
        font.setPointSize(10)
        self.ui_save_action.setFont(font)
        self.ui_open_action = QAction(MainWindow)
        self.ui_open_action.setObjectName(u"ui_open_action")
        self.ui_open_action.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.ui_run_all_btn = QPushButton(self.groupBox)
        self.ui_run_all_btn.setObjectName(u"ui_run_all_btn")
        icon = QIcon()
        icon.addFile(u"ICONS:/executeAll.png", QSize(), QIcon.Normal, QIcon.Off)
        self.ui_run_all_btn.setIcon(icon)
        self.ui_run_all_btn.setIconSize(QSize(25, 25))
        self.ui_run_all_btn.setFlat(True)

        self.horizontalLayout_2.addWidget(self.ui_run_all_btn)

        self.ui_run_sel_btn = QPushButton(self.groupBox)
        self.ui_run_sel_btn.setObjectName(u"ui_run_sel_btn")
        icon1 = QIcon()
        icon1.addFile(u"ICONS:/execute.png", QSize(), QIcon.Normal, QIcon.Off)
        self.ui_run_sel_btn.setIcon(icon1)
        self.ui_run_sel_btn.setIconSize(QSize(25, 25))
        self.ui_run_sel_btn.setFlat(True)

        self.horizontalLayout_2.addWidget(self.ui_run_sel_btn)

        self.line_3 = QFrame(self.groupBox)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_2.addWidget(self.line_3)

        self.ui_clear_log_btn = QPushButton(self.groupBox)
        self.ui_clear_log_btn.setObjectName(u"ui_clear_log_btn")
        icon2 = QIcon()
        icon2.addFile(u"ICONS:/clearHistory.png", QSize(), QIcon.Normal, QIcon.Off)
        self.ui_clear_log_btn.setIcon(icon2)
        self.ui_clear_log_btn.setIconSize(QSize(25, 25))
        self.ui_clear_log_btn.setFlat(True)

        self.horizontalLayout_2.addWidget(self.ui_clear_log_btn)

        self.ui_clear_script_btn = QPushButton(self.groupBox)
        self.ui_clear_script_btn.setObjectName(u"ui_clear_script_btn")
        icon3 = QIcon()
        icon3.addFile(u"ICONS:/clearInput.png", QSize(), QIcon.Normal, QIcon.Off)
        self.ui_clear_script_btn.setIcon(icon3)
        self.ui_clear_script_btn.setIconSize(QSize(25, 25))
        self.ui_clear_script_btn.setFlat(True)

        self.horizontalLayout_2.addWidget(self.ui_clear_script_btn)

        self.ui_clear_both_btn = QPushButton(self.groupBox)
        self.ui_clear_both_btn.setObjectName(u"ui_clear_both_btn")
        icon4 = QIcon()
        icon4.addFile(u"ICONS:/clearAll.png", QSize(), QIcon.Normal, QIcon.Off)
        self.ui_clear_both_btn.setIcon(icon4)
        self.ui_clear_both_btn.setIconSize(QSize(25, 25))
        self.ui_clear_both_btn.setFlat(True)

        self.horizontalLayout_2.addWidget(self.ui_clear_both_btn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addWidget(self.groupBox)

        self.ui_tab_widget = QTabWidget(self.centralwidget)
        self.ui_tab_widget.setObjectName(u"ui_tab_widget")
        self.ui_tab_widget.setTabsClosable(True)
        self.ui_add_tab = QWidget()
        self.ui_add_tab.setObjectName(u"ui_add_tab")
        self.ui_tab_widget.addTab(self.ui_add_tab, "")

        self.verticalLayout.addWidget(self.ui_tab_widget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 567, 26))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuFile.setFont(font)
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.ui_save_action)
        self.menuFile.addAction(self.ui_open_action)

        self.retranslateUi(MainWindow)

        self.ui_tab_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Unreal Script Editor", None))
        self.ui_save_action.setText(QCoreApplication.translate("MainWindow", u"Save as...", None))
        self.ui_open_action.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.groupBox.setTitle("")
#if QT_CONFIG(tooltip)
        self.ui_run_all_btn.setToolTip(QCoreApplication.translate("MainWindow", u"execute all commands", None))
#endif // QT_CONFIG(tooltip)
        self.ui_run_all_btn.setText("")
#if QT_CONFIG(tooltip)
        self.ui_run_sel_btn.setToolTip(QCoreApplication.translate("MainWindow", u"execute selected commands", None))
#endif // QT_CONFIG(tooltip)
        self.ui_run_sel_btn.setText("")
#if QT_CONFIG(tooltip)
        self.ui_clear_log_btn.setToolTip(QCoreApplication.translate("MainWindow", u"clear unreal log", None))
#endif // QT_CONFIG(tooltip)
        self.ui_clear_log_btn.setText("")
#if QT_CONFIG(tooltip)
        self.ui_clear_script_btn.setToolTip(QCoreApplication.translate("MainWindow", u"clear input script", None))
#endif // QT_CONFIG(tooltip)
        self.ui_clear_script_btn.setText("")
#if QT_CONFIG(tooltip)
        self.ui_clear_both_btn.setToolTip(QCoreApplication.translate("MainWindow", u"clear all", None))
#endif // QT_CONFIG(tooltip)
        self.ui_clear_both_btn.setText("")
        self.ui_tab_widget.setTabText(self.ui_tab_widget.indexOf(self.ui_add_tab), QCoreApplication.translate("MainWindow", u"+", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi



def show():
    import sys

    app = QApplication.instance() or QApplication(sys.argv)

    main_window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(main_window)
    main_window.show()

    app.exec_()
    # if RUNNING_IN_UNREAL:
    #     unreal.parent_external_window_to_slate(int(WINDOW.winId()))

    return main_window

# if __name__ == "__main__":
#     show()