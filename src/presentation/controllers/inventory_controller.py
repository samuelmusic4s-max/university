from PySide6.QtGui import QStandardItemModel, QStandardItem
from ui.views.inventory_view import InventoryView
from src.application.services.register_product_use_case import RegisterProductUseCase
from src.application.services.find_all_products_use_case import FindAllProductsUseCase
from src.domain.entities.product import Product
from ui.views.product_dialog import ProductDialog
from src.domain.value_objects.non_empty_string import NonEmptyString
from src.application.services.update_product_use_case import UpdateProductUseCase
from src.application.services.delete_product_use_case import DeleteProductUseCase
from PySide6.QtWidgets import QMessageBox, QWidget, QHBoxLayout, QPushButton
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon


class InventoryController:
    def __init__(
        self,
        view: InventoryView,
        register_uc: RegisterProductUseCase,
        find_all_uc: FindAllProductsUseCase,
        update_uc: UpdateProductUseCase,
        delete_uc: DeleteProductUseCase,
    ):
        self.list_model = QStandardItemModel()
        self.view = view
        self.register_uc = register_uc
        self.find_all_uc = find_all_uc
        self.update_uc = update_uc
        self.delete_uc = delete_uc
        self.view.ui.listView.setModel(self.list_model)

        self.view.ui.listView.setIconSize(QSize(64, 64))

        self.view.ui.pushButton_2.clicked.connect(self.open_add_dialog)
        self.view.ui.pushButton.clicked.connect(self.search_products)
        self.view.ui.lineEdit.textChanged.connect(self.search_products)

        self.load_products()

    def open_add_dialog(self):
        dialog = ProductDialog(self.view)
        if dialog.exec():
            data = dialog.get_data()
            try:
                prod = Product(
                    product_id=NonEmptyString(data["id"]),
                    categories=[NonEmptyString(c) for c in data["categories"]],
                    price=data["price"],
                    description=NonEmptyString(data["description"]),
                    name=NonEmptyString(data["name"]),
                    state=NonEmptyString(data["state"]),
                    img_url=NonEmptyString(data["img_url"]),
                )
                self.register_uc.execute(prod)
                self.load_products()
            except Exception as e:
                QMessageBox.warning(self.view, "Error de validación", str(e))

    def load_products(self, products: list[Product] | None = None):
        if products is None:
            products = self.find_all_uc.execute() or []
        self.list_model.clear()
        for prod in products:
            item = QStandardItem(
                f"[{prod.product_id}] {prod.name} - ${prod.price:,.2f} ({prod.state})"
            )
            item.setEditable(False)
            item.setSizeHint(QSize(0, 80))
            item.setIcon(QIcon(str(prod.img_url)))

            self.list_model.appendRow(item)
            index = self.list_model.indexFromItem(item)

            row_widget = QWidget()
            row_widget.setStyleSheet("background-color: transparent;")
            item_layout = QHBoxLayout(row_widget)
            item_layout.setContentsMargins(0, 0, 12, 0)
            item_layout.addStretch()

            edit_btn = QPushButton("Editar")
            delete_btn = QPushButton("Eliminar")
            delete_btn.setStyleSheet("background-color: #C62828; color:#FFFFFF;")
            delete_btn.clicked.connect(
                lambda checked=False, p=prod: self.delete_product(p)
            )

            edit_btn.setStyleSheet("background-color: #6B5724; color: #FFFFFF")
            edit_btn.clicked.connect(
                lambda checked=False, p=prod: self.open_edit_dialog(p)
            )
            item_layout.addWidget(edit_btn)
            item_layout.addWidget(delete_btn)
            self.view.ui.listView.setIndexWidget(index, row_widget)

    def search_products(self):
        data = self.view.ui.lineEdit.text().strip().lower()
        products = self.find_all_uc.execute() or []
        filtered_products = [
            prod
            for prod in products
            if any(data.lower() in str(v).lower() for v in vars(prod).values())
        ]
        self.load_products(filtered_products)

    def open_edit_dialog(self, product: Product) -> None:
        dialog = ProductDialog(self.view, product)
        if dialog.exec():
            data = dialog.get_data()
            try:
                prod = Product(
                    product_id=NonEmptyString(data["id"]),
                    categories=[NonEmptyString(c) for c in data["categories"]],
                    price=data["price"],
                    description=NonEmptyString(data["description"]),
                    name=NonEmptyString(data["name"]),
                    state=NonEmptyString(data["state"]),
                    img_url=NonEmptyString(data["img_url"]),
                )
                self.update_uc.execute(prod)
                self.load_products()
            except Exception as e:
                QMessageBox.warning(self.view, "Error de validación", str(e))

    def delete_product(self, product: Product) -> None:
        confirm = QMessageBox.question(
            self.view,
            "Confirmar eliminación",
            f"¿Estás seguro de eliminar '{product.name}' ({product.product_id})?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                self.delete_uc.execute(product.product_id)
                self.load_products()
            except Exception as e:
                QMessageBox.warning(self.view, "Error al eliminar", str(e))
