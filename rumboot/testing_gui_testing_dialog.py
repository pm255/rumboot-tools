# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testing_gui_testing_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TestingDialog(object):
    def setupUi(self, TestingDialog):
        TestingDialog.setObjectName("TestingDialog")
        TestingDialog.resize(838, 593)
        self.verticalLayout = QtWidgets.QVBoxLayout(TestingDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.test_progres_bar = QtWidgets.QProgressBar(TestingDialog)
        self.test_progres_bar.setProperty("value", 24)
        self.test_progres_bar.setObjectName("test_progres_bar")
        self.verticalLayout.addWidget(self.test_progres_bar)
        self.test_name_line_edit = QtWidgets.QLineEdit(TestingDialog)
        self.test_name_line_edit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.test_name_line_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.test_name_line_edit.setReadOnly(True)
        self.test_name_line_edit.setObjectName("test_name_line_edit")
        self.verticalLayout.addWidget(self.test_name_line_edit)
        self.log_plain_text_edit = QtWidgets.QPlainTextEdit(TestingDialog)
        self.log_plain_text_edit.setReadOnly(True)
        self.log_plain_text_edit.setObjectName("log_plain_text_edit")
        self.verticalLayout.addWidget(self.log_plain_text_edit)
        self.buttonBox = QtWidgets.QDialogButtonBox(TestingDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(TestingDialog)
        self.buttonBox.accepted.connect(TestingDialog.accept)
        self.buttonBox.rejected.connect(TestingDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TestingDialog)

    def retranslateUi(self, TestingDialog):
        _translate = QtCore.QCoreApplication.translate
        TestingDialog.setWindowTitle(_translate("TestingDialog", "Процесс тестирования"))
