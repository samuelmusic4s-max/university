from PySide6.QtWidgets import (
    QDialog,
    QWidget,
    QFormLayout,
    QDialogButtonBox,
    QPlainTextDocumentLayout,
    QPlainTextEdit,
    QSpinBox,
    QLineEdit,
    QComboBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextDocument
from src.domain.entities.person import Person


class PersonDialog(QDialog):
    def __init__(self, parent: QWidget | None = None, person: Person | None = None):
        super().__init__(parent)
        self.setWindowTitle("Registrar Persona")

        self.person_id_input = QLineEdit()
        self.person_id_input.setPlaceholderText("Ingrese el id del tercero")

        self.identificacion_input = QLineEdit()
        self.identificacion_input.setPlaceholderText(
            "Ingrese la identificación del tercero"
        )

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ingrese el nombre del tercero")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Ingrese el correo electrónico del tercero")

        self.postal_code_input = QSpinBox()
        self.postal_code_input.setMinimum(1)
        self.postal_code_input.setMaximum(999)
        self.postal_code_input.setValue(57)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Ingrese el número de telefono del tercero")

        self.address_input = QPlainTextEdit()
        self.address_input.setPlaceholderText("Ingrese las direcciones separadas por ;")

        doc = QTextDocument(self.address_input)
        layout = QPlainTextDocumentLayout(doc)
        doc.setDocumentLayout(layout)
        self.address_input.setDocument(doc)
        self.address_input.setMaximumHeight(80)

        self.role_input = QComboBox()
        self.role_input.addItems(["Cliente", "Proveedor", "Artesano", "Empleado"])

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        form_layout = QFormLayout()
        form_layout.addRow("ID: ", self.person_id_input)
        form_layout.addRow("Identificacion:", self.identificacion_input)
        form_layout.addRow("Nombre:", self.name_input)
        form_layout.addRow("Correo electrónico:", self.email_input)
        form_layout.addRow("Código Postal:", self.postal_code_input)
        form_layout.addRow("Número de teléfono:", self.phone_input)
        form_layout.addRow("Dirección (;):", self.address_input)
        form_layout.addRow("Rol:", self.role_input)
        form_layout.addRow(self.buttons)

        self.setLayout(form_layout)

        if person is not None:
            self.person_id_input.setText(person.person_id)
            self.person_id_input.setReadOnly(True)
            self.setWindowTitle("Editar Persona")

            self.identificacion_input.setText(str(person.identification))
            self.name_input.setText(str(person.name))
            self.email_input.setText(str(person.email))
            self.postal_code_input.setValue(int(person.phone.postal_code))
            self.phone_input.setText(str(person.phone.value))
            self.address_input.setPlainText(str(";".join(a for a in person.address)))
            self.role_input.setCurrentText(str(person.role))

    def get_data(self) -> dict[str, list[str] | str | float | dict[str, str]]:
        return {
            "id": self.person_id_input.text().strip(),
            "identification": self.identificacion_input.text().strip(),
            "name": self.name_input.text().strip(),
            "email": self.email_input.text().strip(),
            "phone": {
                "value": self.phone_input.text().strip(),
                "postal_code": str(self.postal_code_input.value()),
            },
            "address": [
                str(a.strip())
                for a in self.address_input.toPlainText().split(";")
                if a.strip()
            ],
            "role": self.role_input.currentText(),
        }
