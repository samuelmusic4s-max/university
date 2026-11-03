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
    def __init__(
        self,
        mode: str,
        pay: EmittedPay | ReceivedPay | None = None,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)

        self.mode = mode

        self.pay_id_input = QLineEdit()
        self.pay_id_input.setPlaceholderText("Ingrese el ID del pago")
        self.specific_id_input = QLineEdit()
        self.specific_id_input.setPlaceholderText("Ingrese el ID de compra o venta")

        self.person_id_input = QLineEdit()
        self.person_id_input.setPlaceholderText(
            "Ingrese el ID del tercero (ej. PER-01)"
        )

        self.date_input = QLineEdit(QDate.currentDate().toString("yyyy-MM-dd"))

        self.amount_input = QDoubleSpinBox()
        self.amount_input.setMaximum(999999999.0)

        self.method_input = QComboBox()
        self.method_input.addItems(
            ["Efectivo", "Transferencia", "Tarjeta", "Nequi/Daviplata"]
        )

        self.reason_input = QLineEdit()
        self.reason_input.setPlaceholderText("Ingrese el concepto del pago")

        self.is_advance_input = QCheckBox("¿Es un anticipo / abono?")

        self.url_input = QLineEdit()
        self.url_input.setReadOnly(True)

        self.select_img_btn = QPushButton("Seleccionar Soporte...")
        self.img_preview_lbl = QLabel()

        self.select_img_btn.clicked.connect(self.select_image)

        self.recipient_account_input = QLineEdit()
        self.recipient_account_input.setPlaceholderText(
            "Cuenta destino (ej. Nequi 300...)"
        )

        self.interest_dial = QDial()
        self.interest_dial.setMinimum(0)
        self.interest_dial.setMaximum(100)
        self.interest_dial.setValue(0)
        self.interest_dial.setNotchesVisible(True)
        self.interest_dial.setFixedSize(60, 60)

        self.interest_lbl = QLabel("0% (Neto: $0:00)")
        self.interest_dial.valueChanged.connect(self._update_net_label)
        self.amount_input.valueChanged.connect(self._update_net_label)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        form_layout = QFormLayout()
        form_layout.addRow("ID Pago:", self.pay_id_input)
        form_layout.addRow(
            "ID Compra:" if self.mode == "emitted" else "ID Venta:",
            self.specific_id_input,
        )
        form_layout.addRow("ID Tercero:", self.person_id_input)
        form_layout.addRow("Fecha:", self.date_input)
        form_layout.addRow("Monto:", self.amount_input)
        form_layout.addRow("Método:", self.method_input)
        form_layout.addRow("Concepto:", self.reason_input)
        form_layout.addRow("", self.is_advance_input)

        if self.mode == "emitted":
            self.setWindowTitle("Registrar Compra (Pago Emitido)")
            form_layout.addRow("Cuenta Destino:", self.recipient_account_input)
        else:
            self.setWindowTitle("Registrar Venta (Pago Recibido)")
            dial_layout = QHBoxLayout()
            dial_layout.addWidget(self.interest_dial)
            dial_layout.addWidget(self.interest_lbl)
            form_layout.addRow("Interés (%)", dial_layout)

        form_layout.addRow("Archivo Soporte (Opcional):", self.url_input)
        form_layout.addRow("", self.select_img_btn)
        form_layout.addRow("Vista Previa:", self.img_preview_lbl)
        form_layout.addRow(self.buttons)
        self.setLayout(form_layout)

        if pay is not None:
            self.setWindowTitle("Editar Soporte")
            self.pay_id_input.setText(str(pay.pay_id))
            self.pay_id_input.setReadOnly(True)
            self.specific_id_input.setReadOnly(True)
            self.person_id_input.setText(str(pay.person_id))
            self.date_input.setText(str(pay.date))
            self.amount_input.setValue(float(pay.amount))
            self.method_input.setCurrentText(str(pay.method))
            self.reason_input.setText(str(pay.reason))
            self.is_advance_input.setChecked(bool(pay.is_advance))
            self.url_input.setText(str(pay.url))

            if isinstance(pay, EmittedPay):
                self.specific_id_input.setText(str(pay.pay_emitted_id))
                self.recipient_account_input.setText(str(pay.recipient_account))

            elif isinstance(pay, ReceivedPay):
                self.specific_id_input.setText(str(pay.received_pay_id))
                self.interest_dial.setValue(int(pay.interest))

    def _update_net_label(self):
        amt = self.amount_input.value()
        pct = self.interest_dial.value()
        net = amt * (1 + pct / 100.0)
        self.interest_lbl.setText(f"{pct}% (Neto: ${net:,.2f})")

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar soporte",
            "",
            "Imágenes (*.png *.jpg *.jpeg *.webp *.bmp *.svg)",
        )
        if file_path:
            self.url_input.setText(file_path)
            pixmap = QPixmap(file_path)
            self.img_preview_lbl.setPixmap(
                pixmap.scaled(
                    120,
                    120,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

    def get_data(self) -> dict[str, str | float]:
        amt = float(self.amount_input.value())
        pct = float(self.interest_dial.value()) if self.mode == "received" else 0.0
        return {
            "pay_id": self.pay_id_input.text().strip(),
            "specific_id": self.specific_id_input.text().strip(),
            "person_id": self.person_id_input.text().strip(),
            "date": self.date_input.text().strip(),
            "url": self.url_input.text().strip(),
            "amount": amt,
            "method": self.method_input.currentText(),
            "reason": self.reason_input.text().strip(),
            "is_advance": self.is_advance_input.isChecked(),
            "recipient_account": self.recipient_account_input.text().strip(),
            "interest": pct,
            "net_amount": amt * (1 + pct / 100.0),
        }
