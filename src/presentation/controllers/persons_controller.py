from ui.views.persons_view import PersonsView
from src.application.services.delete_person_use_case import DeletePersonUseCase
from src.application.services.find_all_person_use_case import FindAllPersonUseCase
from src.application.services.find_by_id_person_use_case import FindByIdPersonUseCase
from src.application.services.find_by_ids_person_use_case import FindByIdsPersonUseCase
from src.application.services.update_person_use_case import UpdatePersonUseCase
from src.application.services.save_person_use_case import SavePersonUseCase
from ui.views.person_dialog import PersonDialog
from src.domain.entities.person import Person
from src.domain.value_objects.phone import Phone
from src.domain.value_objects.non_empty_string import NonEmptyString
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QMessageBox,
    QWidget,
    QHBoxLayout,
    QPushButton,
    QInputDialog,
)


class PersonController:
    def __init__(
        self,
        view: PersonsView,
        register_uc: SavePersonUseCase,
        find_all_uc: FindAllPersonUseCase,
        update_uc: UpdatePersonUseCase,
        delete_uc: DeletePersonUseCase,
    ):
        self.list_model = QStandardItemModel()
        self.view = view
        self.register_uc = register_uc
        self.find_all_uc = find_all_uc
        self.update_uc = update_uc
        self.delete_uc = delete_uc
        self.view.ui.listView.setModel(self.list_model)

        self.view.ui.pushButton_2.clicked.connect(self.open_add_dialog)
        self.view.ui.pushButton.clicked.connect(self.search_persons)
        self.view.ui.lineEdit.textChanged.connect(self.search_persons)
        self.view.ui.pushButton_3.clicked.connect(self.filter_persons)
        self.load_persons()

    def open_add_dialog(self):
        dialog = PersonDialog(self.view)
        if dialog.exec():
            data = dialog.get_data()
            try:
                person = Person(
                    person_id=NonEmptyString(data["id"]),
                    identification=NonEmptyString(data["identification"]),
                    name=NonEmptyString(data["name"]),
                    email=NonEmptyString(data["email"]),
                    phone=Phone(
                        value=NonEmptyString(data["phone"]["value"]),
                        postal_code=NonEmptyString(data["phone"]["postal_code"]),
                    ),
                    address=[NonEmptyString(a) for a in data["address"]],
                    role=NonEmptyString(data["role"]),
                )
                self.register_uc.execute(person)
                self.load_persons()
            except Exception as e:
                QMessageBox.warning(self.view, "Error de validación", str(e))

    def load_persons(self, persons: list[Person] | None = None):
        if persons is None:
            persons = self.find_all_uc.execute() or []
        self.list_model.clear()
        for person in persons:
            item = QStandardItem(
                f"[{person.person_id}] {person.name} ({person.role})\n"
                f"ID: {person.identification} | Tel: +{person.phone.postal_code} {person.phone.value} | {person.email}"
            )
            item.setEditable(False)
            item.setSizeHint(QSize(0, 80))

            self.list_model.appendRow(item)
            index = self.list_model.indexFromItem(item)

            row_widget = QWidget()
            row_widget.setStyleSheet("background-color: transparent;")
            item_layout = QHBoxLayout(row_widget)
            item_layout.setContentsMargins(0, 0, 12, 0)
            item_layout.addStretch()

            edit_btn = QPushButton("Editar")
            delete_btn = QPushButton("Eliminar")
            delete_btn.setStyleSheet("background-color: #C62828; color: #FFFFFF")
            delete_btn.clicked.connect(
                lambda checked=False, p=person: self.delete_person(p)
            )

            edit_btn.setStyleSheet("background-color : #6B5724; color: #FFFFFF;")
            edit_btn.clicked.connect(
                lambda checked=False, p=person: self.open_edit_dialog(p)
            )
            item_layout.addWidget(edit_btn)
            item_layout.addWidget(delete_btn)
            self.view.ui.listView.setIndexWidget(index, row_widget)

    def search_persons(self):
        data = self.view.ui.lineEdit.text().strip().lower()
        persons = self.find_all_uc.execute() or []
        filtered_persons = [
            pers
            for pers in persons
            if any(data.lower() in str(v).lower() for v in vars(pers).values())
        ]
        self.load_persons(filtered_persons)

    def open_edit_dialog(self, person: Person) -> None:
        dialog = PersonDialog(self.view, person)
        if dialog.exec():
            data = dialog.get_data()
            try:
                pers = Person(
                    person_id=NonEmptyString(data["id"]),
                    identification=NonEmptyString(data["identification"]),
                    name=NonEmptyString(data["name"]),
                    email=NonEmptyString(data["email"]),
                    phone=Phone(
                        value=NonEmptyString(data["phone"]["value"]),
                        postal_code=NonEmptyString(data["phone"]["postal_code"]),
                    ),
                    address=[NonEmptyString(a) for a in data["address"]],
                    role=NonEmptyString(data["role"]),
                )
                self.update_uc.execute(pers)
                self.load_persons()
            except Exception as e:
                QMessageBox.warning(self.view, "Error de validación", str(e))

    def delete_person(self, person: Person) -> None:
        confirm = QMessageBox.question(
            self.view,
            "Confirmar eliminación",
            f"¿Estás seguro de eliminar [{person.person_id}] {person.name} ({person.role}) ",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                self.delete_uc.execute(person.person_id)
                self.load_persons()
            except Exception as e:
                QMessageBox.warning(self.view, "Error al eliminar", str(e))

    def filter_persons(self):
        roles = ["Todos", "Cliente", "Proveedor", "Artesano", "Empleado"]
        role, ok = QInputDialog.getItem(
            self.view, "Filtrar por rol", "Rol:", roles, 0, False
        )
        if ok:
            persons = self.find_all_uc.execute() or []
            if role != "Todos":
                persons = [p for p in persons if str(p.role) == role]
            self.load_persons(persons)
