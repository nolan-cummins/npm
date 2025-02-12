# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'savepointtHoPAu.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFormLayout, QLabel, QLineEdit,
    QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(320, 120)
        Dialog.setMinimumSize(QSize(320, 120))
        Dialog.setMaximumSize(QSize(320, 120))
        self.formLayout = QFormLayout(Dialog)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.label)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.name_input = QLineEdit(Dialog)
        self.name_input.setObjectName(u"name_input")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.name_input)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Save)

        self.formLayout.setWidget(3, QFormLayout.SpanningRole, self.buttonBox)

        self.comboBox = QComboBox(Dialog)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setEditable(False)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.comboBox)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\">Save Point</p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Name", None))
#if QT_CONFIG(tooltip)
        self.buttonBox.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Save</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.comboBox.setItemText(0, "")
        self.comboBox.setItemText(1, QCoreApplication.translate("Dialog", u"Save Point 1", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Dialog", u"Save Point 2", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Dialog", u"Save Point 3", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("Dialog", u"Save Point 4", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("Dialog", u"Save Point 5", None))

        self.comboBox.setCurrentText("")
        self.comboBox.setPlaceholderText("")
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Select", None))
    # retranslateUi

