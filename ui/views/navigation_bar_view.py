from PySide6.QtWidgets import QWidget
from ui.generated.ui_barra_navegacion import Ui_Form
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from pathlib import Path

icons_dir = Path(__file__).resolve().parents[2] / "assets" / "icons"


class NavigationBarView(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setMinimumWidth(170)
        self.ui.toolButton.setIcon(QIcon(str(icons_dir / "inventory.svg")))
        self.ui.toolButton_2.setIcon(QIcon(str(icons_dir / "persons.svg")))
        self.ui.toolButton_3.setIcon(QIcon(str(icons_dir / "analytics.svg")))
        self.ui.toolButton_4.setIcon(QIcon(str(icons_dir / "supports.svg")))
