from ui.views.main_window import MainWindow
from src.infrastructure.repositories.sqlite_product_repository import (
    SqliteProductRepository,
)
from src.infrastructure.repositories.sqlite_person_repository import (
    SqlitePersonRepository,
)
from src.infrastructure.repositories.sqlite_emitted_pay import SqliteEmittedPay
from src.infrastructure.repositories.sqlite_received_pay_repository import (
    SqliteReceivedPay,
)
from src.application.services.register_product_use_case import RegisterProductUseCase
from src.application.services.find_all_products_use_case import FindAllProductsUseCase
from src.presentation.controllers.inventory_controller import InventoryController
from src.application.services.update_product_use_case import UpdateProductUseCase
from src.application.services.delete_product_use_case import DeleteProductUseCase
from src.application.services.save_person_use_case import SavePersonUseCase
from src.application.services.update_person_use_case import UpdatePersonUseCase
from src.application.services.delete_person_use_case import DeletePersonUseCase
from src.application.services.find_all_person_use_case import FindAllPersonUseCase
from src.presentation.controllers.persons_controller import PersonController
from src.application.services.save_emitted_pay_use_case import SaveEmittedPayUseCase
from src.application.services.find_all_emitted_pay_use_case import (
    FindAllEmittedPayUseCase,
)
from src.application.services.update_emitted_pay_use_case import UpdateEmittedPayUseCase
from src.application.services.delete_emitted_pay_use_case import DeleteEmittedPayUseCase
from src.application.services.save_received_pay_use_case import SaveReceivedPayUseCase
from src.application.services.find_all_received_pay_use_case import (
    FindAllReceivedPayUseCase,
)
from src.application.services.update_received_pay_use_case import (
    UpdateReceivedPayUseCase,
)
from src.application.services.delete_received_pay_use_case import (
    DeleteReceivedPayUseCase,
)
from src.presentation.controllers.registers_controller import RegistersController
from src.presentation.controllers.data_controller import DataController


class AppHandler:
    def __init__(self, window: MainWindow):
        self.window = window
        self._setup_inventory()
        self._setup_persons()
        self._setup_registers()
        self._setup_data()

        self.window.navBar.ui.toolButton_3.clicked.connect(
            self.data_controller.refresh_analytics
        )
        self.window.navBar.ui.toolButton_4.clicked.connect(
            self.registers_controller.load_pays
        )

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

    def _setup_registers(self):
        emitted_repo = SqliteEmittedPay()
        received_repo = SqliteReceivedPay()

        self.registers_controller = RegistersController(
            self.window.registersView,
            SaveEmittedPayUseCase(emitted_repo),
            FindAllEmittedPayUseCase(emitted_repo),
            UpdateEmittedPayUseCase(emitted_repo),
            DeleteEmittedPayUseCase(emitted_repo),
            SaveReceivedPayUseCase(received_repo),
            FindAllReceivedPayUseCase(received_repo),
            UpdateReceivedPayUseCase(received_repo),
            DeleteReceivedPayUseCase(received_repo),
        )

    def _setup_data(self):
        product_repo = SqliteProductRepository()
        persons_repo = SqlitePersonRepository()
        emitted_repo = SqliteEmittedPay()
        received_repo = SqliteReceivedPay()

        self.data_controller = DataController(
            self.window.dataView,
            FindAllProductsUseCase(product_repo),
            FindAllPersonUseCase(persons_repo),
            FindAllEmittedPayUseCase(emitted_repo),
            FindAllReceivedPayUseCase(received_repo),
        )
