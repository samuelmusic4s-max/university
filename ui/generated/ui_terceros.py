# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Terceros.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QListView, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(740, 592)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(16, 16, 16, 16)
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditFind))
        self.pushButton.setIcon(icon)

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_3 = QPushButton(self.widget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout.addWidget(self.pushButton_3)

        self.pushButton_2 = QPushButton(self.widget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.listView = QListView(self.widget)
        self.listView.setObjectName(u"listView")

        self.verticalLayout.addWidget(self.listView)


        self.verticalLayout_2.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Terceros", None))
        self.pushButton.setText("")
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"FILTRAR", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"A\u00d1ADIR", None))
    # retranslateUi

