from PySide6.QtWidgets import QWidget, QHBoxLayout, QStackedLayout
from ui.views.navigation_bar_view import NavigationBarView
from ui.views.data_view import DataView
from ui.views.registers_view import RegistersView
from ui.views.persons_view import PersonsView
from ui.views.inventory_view import InventoryView


class MainWindow(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.navBar = NavigationBarView()
        self.navBar.setMaximumWidth(170)

        self.dataView = DataView()

        self.registersView = RegistersView()

        self.personsView = PersonsView()

        self.inventoryView = InventoryView()

        self.pagesLayout = QStackedLayout()

        self.pagesLayout.addWidget(self.inventoryView)
        self.pagesLayout.addWidget(self.personsView)
        self.pagesLayout.addWidget(self.dataView)
        self.pagesLayout.addWidget(self.registersView)

        self.rootLayout = QHBoxLayout()
        self.rootLayout.setContentsMargins(0, 0, 0, 0)
        self.rootLayout.setSpacing(0)
        self.rootLayout.addWidget(self.navBar)
        self.rootLayout.addLayout(self.pagesLayout)

        self.setLayout(self.rootLayout)

        self.navBar.ui.toolButton.clicked.connect(
            lambda: self.pagesLayout.setCurrentWidget(self.inventoryView)
        )

        self.navBar.ui.toolButton_2.clicked.connect(
            lambda: self.pagesLayout.setCurrentWidget(self.personsView)
        )
        self.navBar.ui.toolButton_3.clicked.connect(
            lambda: self.pagesLayout.setCurrentWidget(self.dataView)
        )
        self.navBar.ui.toolButton_4.clicked.connect(
            lambda: self.pagesLayout.setCurrentWidget(self.registersView)
        )
