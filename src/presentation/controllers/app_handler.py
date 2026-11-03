from ui.views.main_window import MainWindow
from src.infrastructure.repositories.sqlite_product_repository import (
    SqliteProductRepository,
)
from src.infrastructure.repositories.sqlite_person_repository import (
    SqlitePersonRepository,
)
from src.application.services.register_product_use_case import RegisterProductUseCase
from src.application.services.find_all_products_use_case import FindAllProductsUseCase
from src.presentation.controllers.inventory_controller import InventoryController
from src.application.services.update_product_use_case import UpdateProductUseCase
from src.application.services.delete_product_use_case import DeleteProductUseCase
from src.application.services.save_person_use_case import SavePersonUseCase
from src.application.services.update_person_use_case import UpdatePersonUseCase
from src.application.services.find_by_ids_person_use_case import FindByIdsPersonUseCase
from src.application.services.delete_person_use_case import DeletePersonUseCase
from src.application.services.find_all_person_use_case import FindAllPersonUseCase
from src.presentation.controllers.persons_controller import PersonController


class AppHandler:
    def __init__(self, window: MainWindow):
        self.window = window
        self._setup_inventory()
        self._setup_persons()

    def _setup_inventory(self):
        product_repo = SqliteProductRepository()
        register_uc = RegisterProductUseCase(product_repo)
        find_all_uc = FindAllProductsUseCase(product_repo)
        update_uc = UpdateProductUseCase(product_repo)
        delete_uc = DeleteProductUseCase(product_repo)

        self.inventory_controller = InventoryController(
            self.window.inventoryView, register_uc, find_all_uc, update_uc, delete_uc
        )

    def _setup_persons(self):
        persons_repo = SqlitePersonRepository()
        register_uc = SavePersonUseCase(persons_repo)
        find_all_uc = FindAllPersonUseCase(persons_repo)
        update_uc = UpdatePersonUseCase(persons_repo)
        delete_uc = DeletePersonUseCase(persons_repo)

        self.persons_controller = PersonController(
            self.window.personsView, register_uc, find_all_uc, update_uc, delete_uc
        )
