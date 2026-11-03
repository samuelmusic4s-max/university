from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider
from PySide6.QtCore import Qt
from ui.generated.ui_registros import Ui_Form
from pathlib import Path
from PySide6.QtGui import QIcon


search_icon = Path(__file__).resolve().parents[2] / "assets" / "icons" / "search.svg"


class RegistersView(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton.setIcon(QIcon(str(search_icon)))

        self.preview_layout = QVBoxLayout(self.ui.widget_2)
        self.image_label = QLabel("Seleccione un soporte")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(80)
        self.slider.setMaximum(320)
        self.slider.setValue(180)
        self.preview_layout.addWidget(self.image_label)
        self.preview_layout.addWidget(QLabel("Zoom:"))
        self.preview_layout.addWidget(self.slider)
