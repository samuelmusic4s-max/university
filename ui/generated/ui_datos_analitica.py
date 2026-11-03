# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Datos-Analitica.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(852, 592)
        Form.setStyleSheet(u"")
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setSpacing(12)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(16, 16, 16, 16)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"")

        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"")

        self.verticalLayout.addWidget(self.label_2)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.pushButton_9 = QPushButton(self.widget)
        self.pushButton_9.setObjectName(u"pushButton_9")

        self.horizontalLayout.addWidget(self.pushButton_9)

        self.pushButton_8 = QPushButton(self.widget)
        self.pushButton_8.setObjectName(u"pushButton_8")

        self.horizontalLayout.addWidget(self.pushButton_8)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.pushButton_7 = QPushButton(self.widget)
        self.pushButton_7.setObjectName(u"pushButton_7")

        self.horizontalLayout_2.addWidget(self.pushButton_7)

        self.comboBox = QComboBox(self.widget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_2.addWidget(self.comboBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setMinimumSize(QSize(120, 90))
        self.widget_2.setMaximumSize(QSize(400, 220))

        self.horizontalLayout_3.addWidget(self.widget_2)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setMinimumSize(QSize(120, 90))
        self.widget_3.setMaximumSize(QSize(400, 220))

        self.horizontalLayout_3.addWidget(self.widget_3)

        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.widget_4.setMinimumSize(QSize(120, 90))
        self.widget_4.setMaximumSize(QSize(400, 220))

        self.horizontalLayout_3.addWidget(self.widget_4)

        self.widget_5 = QWidget(self.widget)
        self.widget_5.setObjectName(u"widget_5")
        sizePolicy.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy)
        self.widget_5.setMinimumSize(QSize(120, 90))
        self.widget_5.setMaximumSize(QSize(400, 220))

        self.horizontalLayout_3.addWidget(self.widget_5)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.widget_6 = QWidget(self.widget)
        self.widget_6.setObjectName(u"widget_6")
        sizePolicy.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy)
        self.widget_6.setMinimumSize(QSize(200, 200))

        self.horizontalLayout_4.addWidget(self.widget_6)

        self.widget_7 = QWidget(self.widget)
        self.widget_7.setObjectName(u"widget_7")
        sizePolicy.setHeightForWidth(self.widget_7.sizePolicy().hasHeightForWidth())
        self.widget_7.setSizePolicy(sizePolicy)
        self.widget_7.setMinimumSize(QSize(200, 200))

        self.horizontalLayout_4.addWidget(self.widget_7)

        self.horizontalLayout_4.setStretch(0, 2)
        self.horizontalLayout_4.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_4)


        self.verticalLayout_3.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Datos y Analitica", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Analisa y gestiona los datos del negocio.", None))
        self.pushButton_9.setText(QCoreApplication.translate("Form", u"EXPORTAR DATOS ", None))
        self.pushButton_8.setText(QCoreApplication.translate("Form", u"IMPORTAR DATOS", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Analisis de datos:", None))
        self.pushButton_7.setText(QCoreApplication.translate("Form", u"FILTRAR", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Form", u"Area", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Form", u"Inventario", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Form", u"Terceros", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Form", u"Compras", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("Form", u"Ventas", None))

    # retranslateUi

