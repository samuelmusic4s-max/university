from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QDoubleSpinBox,
    QComboBox,
    QDialogButtonBox,
    QWidget,
    QPlainTextEdit,
    QPlainTextDocumentLayout,
    QPushButton,
    QLabel,
    QFileDialog,
)
from PySide6.QtGui import QTextDocument, QPixmap
from PySide6.QtCore import Qt
from src.domain.entities.product import Product


class ProductDialog(QDialog):
    def __init__(self, parent: QWidget | None = None, product: Product | None = None):
        super().__init__(parent)
        self.setWindowTitle("Registrar Producto")

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Ingrese el id del producto")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ingrese el nombre del producto")

        self.price_input = QDoubleSpinBox()
        self.price_input.setMaximum(999999999.0)

        self.categories_input = QLineEdit()
        self.categories_input.setPlaceholderText(
            "Ingrese las categorías del producto separadas por ;"
        )

        self.state_input = QComboBox()
        self.state_input.addItems(["Disponible", "Agotado", "En fabricación"])
        self.description_input = QPlainTextEdit()
        self.img_url_input = QLineEdit()
        self.img_url_input.setReadOnly(True)

        self.selec_img_btn = QPushButton("Seleccionar Imagen...")
        self.img_preview_lbl = QLabel()

        doc = QTextDocument(self.description_input)
        layout = QPlainTextDocumentLayout(doc)
        doc.setDocumentLayout(layout)

        self.description_input.setDocument(doc)
        self.description_input.setPlaceholderText(
            "Escribe la descripción de la artesanía..."
        )
        self.description_input.setMaximumHeight(100)

        self.selec_img_btn.clicked.connect(self.select_image)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        form_layout = QFormLayout()
        form_layout.addRow("ID:", self.id_input)
        form_layout.addRow("Nombre:", self.name_input)
        form_layout.addRow("Precio:", self.price_input)
        form_layout.addRow("Categorías (;):", self.categories_input)
        form_layout.addRow("Estado:", self.state_input)
        form_layout.addRow("Descripción", self.description_input)
        form_layout.addRow("Ruta Imagen:", self.img_url_input)
        form_layout.addRow("", self.selec_img_btn)
        form_layout.addRow("Vista Previa:", self.img_preview_lbl)
        form_layout.addRow(self.buttons)

        self.setLayout(form_layout)

        if product is not None:
            self.id_input.setText(str(product.product_id))
            self.id_input.setReadOnly(True)
            self.setWindowTitle("Editar Producto")

            self.name_input.setText(str(product.name))
            self.price_input.setValue(float(product.price))
            self.categories_input.setText(";".join(str(c) for c in product.categories))
            self.state_input.setCurrentText(str(product.state))
            self.description_input.setPlainText(str(product.description))
            self.img_url_input.setText(str(product.img_url))

            self.img_url_input.setText(product.img_url)
            pixmap = QPixmap(product.img_url)
            self.img_preview_lbl.setPixmap(
                pixmap.scaled(
                    120,
                    120,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar imagen del producto",
            "",
            "Imágenes (*.png *.jpg *.jpeg *.webp *.bmp *.svg)",
        )
        if file_path:
            self.img_url_input.setText(file_path)
            pixmap = QPixmap(file_path)
            self.img_preview_lbl.setPixmap(
                pixmap.scaled(
                    120,
                    120,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

    def get_data(self) -> dict[str, list[str] | str | float]:
        return {
            "id": self.id_input.text().strip(),
            "price": self.price_input.value(),
            "categories": [
                str(c.strip())
                for c in self.categories_input.text().split(";")
                if c.strip()
            ],
            "state": self.state_input.currentText(),
            "description": self.description_input.toPlainText().strip(),
            "img_url": self.img_url_input.text().strip(),
            "name": self.name_input.text().strip(),
        }
