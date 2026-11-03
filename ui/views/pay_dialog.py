from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QDoubleSpinBox,
    QComboBox,
    QCheckBox,
    QDial,
    QDialogButtonBox,
    QWidget,
    QPushButton,
    QLabel,
    QFileDialog,
    QHBoxLayout,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QDate
from src.domain.entities.emitted_pay import EmittedPay
from src.domain.entities.received_pay import ReceivedPay
from src.domain.entities.person import Person


class PayDialog(QDialog):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent=)