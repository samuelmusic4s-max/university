from PySide6.QtWidgets import QWidget
from ui.generated.ui_datos_analitica import Ui_Form


class DataView(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
