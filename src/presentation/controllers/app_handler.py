from ui.views.main_window import MainWindow
from src.infrastructure.repositories.sqlite_product_repository import (
    SqliteProductRepository,
)
from src.application.services.register_product_use_case import RegisterProductUseCase
from src.application.services.find_all_products_use_case import FindAllProductsUseCase
from src.presentation.controllers.inventory_controller import InventoryController
from src.application.services.update_product_use_case import UpdateProductUseCase
from src.application.services.delete_product_use_case import DeleteProductUseCase


class AppHandler:
    def __init__(self, window: MainWindow):
        self.window = window
        self._setup_inventory()

    def _setup_inventory(self):
        product_repo = SqliteProductRepository()
        register_uc = RegisterProductUseCase(product_repo)
        find_all_uc = FindAllProductsUseCase(product_repo)
        update_uc = UpdateProductUseCase(product_repo)
        delete_uc = DeleteProductUseCase(product_repo)

        self.inventory_controller = InventoryController(
            self.window.inventoryView, register_uc, find_all_uc, update_uc, delete_uc
        )
