# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'barra-navegacion.ui'
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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QSpacerItem, QToolButton,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(172, 602)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(16)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(12, 12, 12, 12)
        self.toolButton = QToolButton(self.widget)
        self.toolButton.setObjectName(u"toolButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton.sizePolicy().hasHeightForWidth())
        self.toolButton.setSizePolicy(sizePolicy)
        self.toolButton.setMinimumSize(QSize(75, 75))
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditPaste))
        self.toolButton.setIcon(icon)
        self.toolButton.setIconSize(QSize(30, 30))
        self.toolButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.verticalLayout.addWidget(self.toolButton)

        self.toolButton_2 = QToolButton(self.widget)
        self.toolButton_2.setObjectName(u"toolButton_2")
        sizePolicy.setHeightForWidth(self.toolButton_2.sizePolicy().hasHeightForWidth())
        self.toolButton_2.setSizePolicy(sizePolicy)
        self.toolButton_2.setMinimumSize(QSize(75, 75))
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.AddressBookNew))
        self.toolButton_2.setIcon(icon1)
        self.toolButton_2.setIconSize(QSize(30, 30))
        self.toolButton_2.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.verticalLayout.addWidget(self.toolButton_2)

        self.toolButton_3 = QToolButton(self.widget)
        self.toolButton_3.setObjectName(u"toolButton_3")
        sizePolicy.setHeightForWidth(self.toolButton_3.sizePolicy().hasHeightForWidth())
        self.toolButton_3.setSizePolicy(sizePolicy)
        self.toolButton_3.setMinimumSize(QSize(75, 75))
        icon2 = QIcon()
        icon2.addFile(u"gemini-svg.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.toolButton_3.setIcon(icon2)
        self.toolButton_3.setIconSize(QSize(35, 35))
        self.toolButton_3.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.verticalLayout.addWidget(self.toolButton_3)

        self.toolButton_4 = QToolButton(self.widget)
        self.toolButton_4.setObjectName(u"toolButton_4")
        sizePolicy.setHeightForWidth(self.toolButton_4.sizePolicy().hasHeightForWidth())
        self.toolButton_4.setSizePolicy(sizePolicy)
        self.toolButton_4.setMinimumSize(QSize(75, 75))
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentNew))
        self.toolButton_4.setIcon(icon3)
        self.toolButton_4.setIconSize(QSize(30, 30))
        self.toolButton_4.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.verticalLayout.addWidget(self.toolButton_4)

        self.verticalSpacer = QSpacerItem(20, 189, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.verticalLayout_2.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.toolButton.setText(QCoreApplication.translate("Form", u"Inventario", None))
        self.toolButton_2.setText(QCoreApplication.translate("Form", u"Terceros", None))
        self.toolButton_3.setText(QCoreApplication.translate("Form", u"Datos y \n"
"Analitica\n"
"", None))
        self.toolButton_4.setText(QCoreApplication.translate("Form", u"Soporte", None))
    # retranslateUi

