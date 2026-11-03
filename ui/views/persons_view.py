from PySide6.QtWidgets import QWidget
from ui.generated.ui_terceros import Ui_Form
from pathlib import Path
from PySide6.QtGui import QIcon


search_icon = Path(__file__).resolve().parents[2] / "assets" / "icons" / "search.svg"


class PersonsView(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton.setIcon(QIcon(str(search_icon)))
