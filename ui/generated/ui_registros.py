# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Registros-.ui'
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
        self.verticalLayout_4 = QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setSpacing(12)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(16, 16, 16, 16)
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.listView = QListView(self.widget)
        self.listView.setObjectName(u"listView")
        self.listView.setMaximumSize(QSize(16777215, 100))

        self.verticalLayout_3.addWidget(self.listView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_3 = QPushButton(self.widget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout.addWidget(self.pushButton_3)

        self.pushButton_7 = QPushButton(self.widget)
        self.pushButton_7.setObjectName(u"pushButton_7")

        self.horizontalLayout.addWidget(self.pushButton_7)

        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditFind))
        self.pushButton.setIcon(icon)

        self.horizontalLayout.addWidget(self.pushButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_6 = QPushButton(self.widget)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.horizontalLayout_2.addWidget(self.pushButton_6)

        self.pushButton_5 = QPushButton(self.widget)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.horizontalLayout_2.addWidget(self.pushButton_5)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.listView_2 = QListView(self.widget)
        self.listView_2.setObjectName(u"listView_2")

        self.verticalLayout.addWidget(self.listView_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 0))
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_3)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setMinimumSize(QSize(220, 200))

        self.verticalLayout_2.addWidget(self.widget_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(1, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.verticalLayout_4.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Soportes", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Manejo de documentos soporte de compras(productos o servicios) y ventas", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"REGISTRAR NUEVO", None))
        self.pushButton_7.setText(QCoreApplication.translate("Form", u"FILTRAR", None))
        self.pushButton.setText("")
        self.pushButton_6.setText(QCoreApplication.translate("Form", u"COMPRAS", None))
        self.pushButton_5.setText(QCoreApplication.translate("Form", u"VENTAS", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"VISTA PREVIA", None))
    # retranslateUi

