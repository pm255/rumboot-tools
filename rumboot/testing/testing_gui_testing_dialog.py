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
        self.test_progress_bar = QtWidgets.QProgressBar(TestingDialog)
        self.test_progress_bar.setObjectName("test_progress_bar")
        self.verticalLayout.addWidget(self.test_progress_bar)
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
        self.dialog_button_box = QtWidgets.QDialogButtonBox(TestingDialog)
        self.dialog_button_box.setOrientation(QtCore.Qt.Horizontal)
        self.dialog_button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.dialog_button_box.setCenterButtons(True)
        self.dialog_button_box.setObjectName("dialog_button_box")
        self.verticalLayout.addWidget(self.dialog_button_box)

        self.retranslateUi(TestingDialog)
        self.dialog_button_box.accepted.connect(TestingDialog.accept)
        self.dialog_button_box.rejected.connect(TestingDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TestingDialog)

    def retranslateUi(self, TestingDialog):
        _translate = QtCore.QCoreApplication.translate
        TestingDialog.setWindowTitle(_translate("TestingDialog", "Процесс тестирования"))
        self.test_progress_bar.setFormat(_translate("TestingDialog", "%v/%m"))