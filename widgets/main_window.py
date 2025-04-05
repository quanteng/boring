# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.UI'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QFrame,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.control_frame = QFrame(self.centralwidget)
        self.control_frame.setObjectName(u"control_frame")
        self.control_frame.setMinimumSize(QSize(300, 0))
        self.control_frame.setFrameShape(QFrame.StyledPanel)
        self.control_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.control_frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(self.control_frame)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget = QWidget(self.groupBox)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.line_dcfq = QLineEdit(self.widget)
        self.line_dcfq.setObjectName(u"line_dcfq")

        self.horizontalLayout_2.addWidget(self.line_dcfq)

        self.btn_load_dcfq = QPushButton(self.widget)
        self.btn_load_dcfq.setObjectName(u"btn_load_dcfq")

        self.horizontalLayout_2.addWidget(self.btn_load_dcfq)


        self.verticalLayout_2.addWidget(self.widget)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.widget_2 = QWidget(self.groupBox)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.line_zdqy = QLineEdit(self.widget_2)
        self.line_zdqy.setObjectName(u"line_zdqy")

        self.horizontalLayout_3.addWidget(self.line_zdqy)

        self.btn_load_zdqy = QPushButton(self.widget_2)
        self.btn_load_zdqy.setObjectName(u"btn_load_zdqy")

        self.horizontalLayout_3.addWidget(self.btn_load_zdqy)


        self.verticalLayout_2.addWidget(self.widget_2)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.control_frame)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.widget_3 = QWidget(self.groupBox_2)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.widget_3)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.spin_grid_size = QSpinBox(self.widget_3)
        self.spin_grid_size.setObjectName(u"spin_grid_size")
        self.spin_grid_size.setMinimum(5)
        self.spin_grid_size.setMaximum(200)
        self.spin_grid_size.setValue(20)

        self.horizontalLayout_4.addWidget(self.spin_grid_size)


        self.verticalLayout_3.addWidget(self.widget_3)

        self.btn_generate_grid = QPushButton(self.groupBox_2)
        self.btn_generate_grid.setObjectName(u"btn_generate_grid")

        self.verticalLayout_3.addWidget(self.btn_generate_grid)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.control_frame)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.widget_4 = QWidget(self.groupBox_3)
        self.widget_4.setObjectName(u"widget_4")
        self.formLayout = QFormLayout(self.widget_4)
        self.formLayout.setObjectName(u"formLayout")
        self.label_4 = QLabel(self.widget_4)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_4)

        self.spin_boring_step = QSpinBox(self.widget_4)
        self.spin_boring_step.setObjectName(u"spin_boring_step")
        self.spin_boring_step.setMinimum(1)
        self.spin_boring_step.setMaximum(20)
        self.spin_boring_step.setValue(2)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.spin_boring_step)

        self.label_5 = QLabel(self.widget_4)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_5)

        self.spin_boring_step_zdqy = QSpinBox(self.widget_4)
        self.spin_boring_step_zdqy.setObjectName(u"spin_boring_step_zdqy")
        self.spin_boring_step_zdqy.setMinimum(1)
        self.spin_boring_step_zdqy.setMaximum(20)
        self.spin_boring_step_zdqy.setValue(1)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.spin_boring_step_zdqy)

        self.label_6 = QLabel(self.widget_4)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_6)

        self.spin_wboring_step = QSpinBox(self.widget_4)
        self.spin_wboring_step.setObjectName(u"spin_wboring_step")
        self.spin_wboring_step.setMinimum(1)
        self.spin_wboring_step.setMaximum(20)
        self.spin_wboring_step.setValue(8)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.spin_wboring_step)

        self.label_7 = QLabel(self.widget_4)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_7)

        self.spin_wboring_step_zdqy = QSpinBox(self.widget_4)
        self.spin_wboring_step_zdqy.setObjectName(u"spin_wboring_step_zdqy")
        self.spin_wboring_step_zdqy.setMinimum(1)
        self.spin_wboring_step_zdqy.setMaximum(20)
        self.spin_wboring_step_zdqy.setValue(4)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.spin_wboring_step_zdqy)

        self.label_8 = QLabel(self.widget_4)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_8)

        self.spin_offset_x = QSpinBox(self.widget_4)
        self.spin_offset_x.setObjectName(u"spin_offset_x")
        self.spin_offset_x.setMinimum(0)
        self.spin_offset_x.setMaximum(20)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.spin_offset_x)

        self.label_9 = QLabel(self.widget_4)
        self.label_9.setObjectName(u"label_9")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_9)

        self.spin_offset_y = QSpinBox(self.widget_4)
        self.spin_offset_y.setObjectName(u"spin_offset_y")
        self.spin_offset_y.setMinimum(0)
        self.spin_offset_y.setMaximum(20)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.spin_offset_y)


        self.verticalLayout_4.addWidget(self.widget_4)

        self.btn_plan_boring = QPushButton(self.groupBox_3)
        self.btn_plan_boring.setObjectName(u"btn_plan_boring")

        self.verticalLayout_4.addWidget(self.btn_plan_boring)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.control_frame)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.cb_show_grid = QCheckBox(self.groupBox_4)
        self.cb_show_grid.setObjectName(u"cb_show_grid")
        self.cb_show_grid.setChecked(True)

        self.verticalLayout_5.addWidget(self.cb_show_grid)

        self.cb_show_boring = QCheckBox(self.groupBox_4)
        self.cb_show_boring.setObjectName(u"cb_show_boring")
        self.cb_show_boring.setChecked(True)

        self.verticalLayout_5.addWidget(self.cb_show_boring)

        self.cb_show_dcfq = QCheckBox(self.groupBox_4)
        self.cb_show_dcfq.setObjectName(u"cb_show_dcfq")
        self.cb_show_dcfq.setChecked(True)

        self.verticalLayout_5.addWidget(self.cb_show_dcfq)

        self.cb_show_zdqy = QCheckBox(self.groupBox_4)
        self.cb_show_zdqy.setObjectName(u"cb_show_zdqy")
        self.cb_show_zdqy.setChecked(True)

        self.verticalLayout_5.addWidget(self.cb_show_zdqy)


        self.verticalLayout.addWidget(self.groupBox_4)

        self.btn_export_results = QPushButton(self.control_frame)
        self.btn_export_results.setObjectName(u"btn_export_results")

        self.verticalLayout.addWidget(self.btn_export_results)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.control_frame)

        self.map_frame = QFrame(self.centralwidget)
        self.map_frame.setObjectName(u"map_frame")
        self.map_frame.setFrameShape(QFrame.StyledPanel)
        self.map_frame.setFrameShadow(QFrame.Raised)
        self.map_layout = QVBoxLayout(self.map_frame)
        self.map_layout.setObjectName(u"map_layout")

        self.horizontalLayout.addWidget(self.map_frame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u94bb\u5b54\u5e03\u70b9\u89c4\u5212\u7cfb\u7edf", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u8f93\u5165", None))
        self.btn_load_dcfq.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u8c03\u67e5\u5206\u533a\u6587\u4ef6", None))
        self.btn_load_zdqy.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u70b9\u533a\u57df\u6587\u4ef6", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u7f51\u683c\u8bbe\u7f6e", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u7f51\u683c\u5927\u5c0f(m)", None))
        self.btn_generate_grid.setText(QCoreApplication.translate("MainWindow", u"\u751f\u6210\u7f51\u683c", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u94bb\u5b54\u89c4\u5212\u53c2\u6570", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u666e\u901a\u94bb\u5b54\u6b65\u957f", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u70b9\u533a\u57df\u6b65\u957f", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u76d1\u6d4b\u4e95\u6b65\u957f", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u70b9\u533a\u57df\u6b65\u957f", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"X\u504f\u79fb\u91cf", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Y\u504f\u79fb\u91cf", None))
        self.btn_plan_boring.setText(QCoreApplication.translate("MainWindow", u"\u89c4\u5212\u94bb\u5b54", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\u56fe\u5c42\u63a7\u5236", None))
        self.cb_show_grid.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u7f51\u683c", None))
        self.cb_show_boring.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u94bb\u5b54", None))
        self.cb_show_dcfq.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u8c03\u67e5\u5206\u533a", None))
        self.cb_show_zdqy.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u91cd\u70b9\u533a\u57df", None))
        self.btn_export_results.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa\u7ed3\u679c", None))
    # retranslateUi

