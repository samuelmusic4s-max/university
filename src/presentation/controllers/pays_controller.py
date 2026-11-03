from pathlib import Path
import pandas as pd
from ui.views.registers_view import RegistersView
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
from PySide6.QtGui import (
    QIcon,
    QImage,
    QPainter,
    QStandardItem,
    QStandardItemModel,
    QPixmap,
    QPdfWriter,
    QTextDocument,
)
from ui.views.pay_dialog import PayDialog
from src.domain.entities.emitted_pay import EmittedPay
from src.domain.entities.received_pay import ReceivedPay
from src.domain.value_objects.non_empty_string import NonEmptyString
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QMessageBox,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QInputDialog,
    QListView,
    QLabel,
    QSlider,
    QFileDialog,
)


class PaysController:
    def __init__(
        self,
        view: RegistersView,
        save_emitted_uc: SaveEmittedPayUseCase,
        find_all_emitted_uc: FindAllEmittedPayUseCase,
        update_emitted_uc: UpdateEmittedPayUseCase,
        delete_emitted_uc: DeleteEmittedPayUseCase,
        save_received_uc: SaveReceivedPayUseCase,
        find_all_received_uc: FindAllReceivedPayUseCase,
        update_received_uc: UpdateReceivedPayUseCase,
        delete_received_uc: DeleteReceivedPayUseCase,
    ):
        self.view = view

        self.save_emitted_uc = save_emitted_uc
        self.find_all_emitted_uc = find_all_emitted_uc
        self.update_emitted_uc = update_emitted_uc
        self.delete_emitted_uc = delete_emitted_uc

        self.save_received_uc = save_received_uc
        self.find_all_received_uc = find_all_received_uc
        self.update_received_uc = update_received_uc
        self.delete_received_uc = delete_received_uc

        self.current_mode = "emitted"
        self.current_image = ""
        self.current_pays: list[EmittedPay | ReceivedPay] = []

        self.top_model = QStandardItemModel()
        self.view.ui.listView.setModel(self.top_model)
        self.view.ui.listView.setFlow(QListView.Flow.LeftToRight)

        self.list_model = QStandardItemModel()
        self.view.ui.listView_2.setModel(self.list_model)
        self.view.ui.listView_2.setIconSize(QSize(48, 48))
        self.view.ui.listView_2.clicked.connect(self._on_item_clicked)

        self.image_label = self.view.image_label
        self.slider = self.view.slider
        self.slider.valueChanged.connect(self.change_zoom)

        self.view.ui.pushButton_6.clicked.connect(lambda: self.switch_mode("emitted"))
        self.view.ui.pushButton_5.clicked.connect(lambda: self.switch_mode("received"))
        self.view.ui.pushButton_3.clicked.connect(self.open_add_dialog)
        self.view.ui.pushButton_7.clicked.connect(self.filter_pays)
        self.view.ui.pushButton.clicked.connect(self.search_pays)
        self.view.ui.lineEdit.textChanged.connect(self.search_pays)

        self.load_pays()

    def switch_mode(self, mode: str):
        self.current_mode = mode
        self.load_pays()

    def load_top_metrics(self):
        compras_list = self.find_all_emitted_uc.execute() or []
        ventas_list = self.find_all_received_uc.execute() or []
        total_compras = sum(p.amount for p in compras_list)
        total_ventas = sum((p.net_amount or p.amount) for p in ventas_list)

        self.top_model.clear()
        texts = [
            f"Compras\n${total_compras:,.2f}",
            f"Ventas\n${total_ventas:,.2f}",
            f"Balance\n${total_ventas - total_compras:,.2f}",
            f"Total Soportes\n{len(compras_list) + len(ventas_list)}",
        ]
        for t in texts:
            item = QStandardItem(t)
            item.setEditable(False)
            item.setSizeHint(QSize(160, 70))
            self.top_model.appendRow(item)

    def _on_item_clicked(self, index):
        row = index.row()
        if 0 <= row < len(self.current_pays):
            self.show_pay_preview(self.current_pays[row])

    def show_pay_preview(self, pay: EmittedPay | ReceivedPay):
        url = str(pay.url)
        if not url or url.endswith("supports.svg") or not Path(url).exists():
            mode = "emitted" if isinstance(pay, EmittedPay) else "received"
            data = {
                "pay_id": str(pay.pay_id),
                "specific_id": (
                    str(pay.pay_emitted_id)
                    if isinstance(pay, EmittedPay)
                    else str(pay.received_pay_id)
                ),
                "person_id": str(pay.person_id),
                "date": str(pay.date),
                "reason": str(pay.reason),
                "method": str(pay.method),
                "is_advance": bool(pay.is_advance),
                "amount": float(pay.amount),
                "recipient_account": (
                    str(pay.recipient_account) if isinstance(pay, EmittedPay) else ""
                ),
                "interest": float(pay.interest) if isinstance(pay, ReceivedPay) else 0.0,
                "net_amount": (
                    float(pay.net_amount or pay.amount)
                    if isinstance(pay, ReceivedPay)
                    else float(pay.amount)
                ),
            }
            url = self.generate_receipt_files(data, mode)
        self.show_image(url)

    def show_image(self, url: str):
        self.current_image = url
        self.change_zoom()

    def change_zoom(self):
        if self.current_image:
            pixmap = QPixmap(self.current_image)
            if not pixmap.isNull():
                size = self.slider.value()
                self.image_label.setPixmap(
                    pixmap.scaled(
                        size,
                        size,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                )

    def generate_receipt_files(self, data: dict, mode: str) -> str:
        supports_dir = Path(__file__).resolve().parents[3] / "assets" / "supports"
        supports_dir.mkdir(parents=True, exist_ok=True)
        tipo = "COMPROBANTE DE COMPRA" if mode == "emitted" else "COMPROBANTE DE VENTA"
        extra = (
            f"<p><b>Cuenta Destino:</b> {data['recipient_account']}</p>"
            if mode == "emitted"
            else f"<p><b>Interés:</b> {data['interest']}% | <b>Neto:</b> ${data['net_amount']:,.2f}</p>"
        )
        html = f"""
        <div style="font-family: sans-serif; padding: 16px;">
            <h2>TIENDA DE ARTESANÍAS - {tipo}</h2>
            <hr/>
            <p><b>ID Pago:</b> {data['pay_id']} | <b>ID Soporte:</b> {data['specific_id']}</p>
            <p><b>Fecha:</b> {data['date']} | <b>Tercero:</b> {data['person_id']}</p>
            <p><b>Concepto:</b> {data['reason']}</p>
            <p><b>Método:</b> {data['method']} ({'Anticipo' if data['is_advance'] else 'Pago Total'})</p>
            <p><b>Monto:</b> ${data['amount']:,.2f}</p>
            {extra}
        </div>
        """
        doc = QTextDocument()
        doc.setHtml(html)
        doc.setTextWidth(420)

        pdf_path = supports_dir / f"soporte_{data['pay_id']}.pdf"
        pdf_writer = QPdfWriter(str(pdf_path))
        doc.print_(pdf_writer)

        img_path = supports_dir / f"soporte_{data['pay_id']}.png"
        image = QImage(420, int(doc.size().height()) + 20, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.white)
        painter = QPainter(image)
        doc.drawContents(painter)
        painter.end()
        image.save(str(img_path))
        return str(img_path)

    def export_pay(self, pay: EmittedPay | ReceivedPay):
        file_path, _ = QFileDialog.getSaveFileName(
            self.view,
            "Guardar Comprobante",
            f"comprobante_{pay.pay_id}.pdf",
            "PDF (*.pdf);;CSV (*.csv)",
        )
        if not file_path:
            return
        row = {k: str(v) for k, v in vars(pay).items()}
        if file_path.endswith(".csv"):
            pd.DataFrame([row]).to_csv(file_path, index=False)
        else:
            writer = QPdfWriter(file_path)
            doc = QTextDocument()
            html = "<h2>Comprobante de Pago</h2>" + "".join(
                f"<p><b>{k}:</b> {v}</p>" for k, v in row.items()
            )
            doc.setHtml(html)
            doc.print_(writer)
        QMessageBox.information(self.view, "Listo", f"Guardado en {file_path}")

    def open_add_dialog(self):
        dialog = PayDialog(mode=self.current_mode, parent=self.view)
        if dialog.exec():
            data = dialog.get_data()
            try:
                url_val = data["url"] or self.generate_receipt_files(
                    data, self.current_mode
                )
                if self.current_mode == "emitted":
                    pay = EmittedPay(
                        person_id=NonEmptyString(data["person_id"]),
                        pay_id=NonEmptyString(data["pay_id"]),
                        date=NonEmptyString(data["date"]),
                        url=NonEmptyString(url_val),
                        amount=float(data["amount"]),
                        method=NonEmptyString(data["method"]),
                        reason=NonEmptyString(data["reason"]),
                        is_advance=bool(data["is_advance"]),
                        pay_emitted_id=NonEmptyString(data["specific_id"]),
                        recipient_account=NonEmptyString(data["recipient_account"]),
                    )
                    self.save_emitted_uc.execute(pay)
                else:
                    received_pay = ReceivedPay(
                        person_id=NonEmptyString(data["person_id"]),
                        pay_id=NonEmptyString(data["pay_id"]),
                        date=NonEmptyString(data["date"]),
                        url=NonEmptyString(url_val),
                        amount=float(data["amount"]),
                        method=NonEmptyString(data["method"]),
                        reason=NonEmptyString(data["reason"]),
                        is_advance=bool(data["is_advance"]),
                        received_pay_id=NonEmptyString(data["specific_id"]),
                        net_amount=float(data["net_amount"]),
                        interest=float(data["interest"]),
                    )
                    self.save_received_uc.execute(received_pay)
                self.load_pays()
            except Exception as e:
                QMessageBox.warning(self.view, "Error de validación", str(e))

    def load_pays(self, pays: list | None = None):
        self.load_top_metrics()
        if pays is None:
            if self.current_mode == "emitted":
                pays = self.find_all_emitted_uc.execute() or []
            else:
                pays = self.find_all_received_uc.execute() or []

        self.current_pays = list(pays)
        self.list_model.clear()
        for pay in pays:
            if isinstance(pay, EmittedPay):
                text = f"[Compra {pay.pay_emitted_id}] ${pay.amount:,.2f} | Tercero: {pay.person_id} | {pay.date}"
            else:
                text = f"[Venta {pay.received_pay_id}] Neto: ${pay.net_amount:,.2f} (Int: {pay.interest}%) | Tercero: {pay.person_id}"

            item = QStandardItem(text)
            item.setEditable(False)
            item.setSizeHint(QSize(0, 75))
            item.setIcon(QIcon(str(pay.url)))
            self.list_model.appendRow(item)
            index = self.list_model.indexFromItem(item)

            row_widget = QWidget()
            row_widget.setStyleSheet("background-color: transparent;")
            item_layout = QHBoxLayout(row_widget)
            item_layout.setContentsMargins(0, 0, 12, 0)
            item_layout.addStretch()

            view_btn = QPushButton("Ver")
            pdf_btn = QPushButton("PDF/CSV")
            edit_btn = QPushButton("Editar")
            delete_btn = QPushButton("Eliminar")
            edit_btn.setStyleSheet("background-color: #6B5724; color: #FFFFFF;")
            delete_btn.setStyleSheet("background-color: #C62828; color: #FFFFFF;")

            view_btn.clicked.connect(
                lambda checked=False, p=pay: self.show_pay_preview(p)
            )
            pdf_btn.clicked.connect(lambda checked=False, p=pay: self.export_pay(p))
            edit_btn.clicked.connect(
                lambda checked=False, p=pay: self.open_edit_dialog(p)
            )
            delete_btn.clicked.connect(lambda checked=False, p=pay: self.delete_pay(p))

            item_layout.addWidget(view_btn)
            item_layout.addWidget(pdf_btn)
            item_layout.addWidget(edit_btn)
            item_layout.addWidget(delete_btn)
            self.view.ui.listView_2.setIndexWidget(index, row_widget)

    def open_edit_dialog(self, pay: EmittedPay | ReceivedPay):
        dialog = PayDialog(mode=self.current_mode, pay=pay, parent=self.view)
        if dialog.exec():
            data = dialog.get_data()
            try:
                url_val = (
                    data["url"]
                    if data["url"] and not str(data["url"]).endswith("supports.svg")
                    else self.generate_receipt_files(data, self.current_mode)
                )
                if self.current_mode == "emitted":
                    updated_emitted = EmittedPay(
                        person_id=NonEmptyString(data["person_id"]),
                        pay_id=NonEmptyString(data["pay_id"]),
                        date=NonEmptyString(data["date"]),
                        url=NonEmptyString(url_val),
                        amount=float(data["amount"]),
                        method=NonEmptyString(data["method"]),
                        reason=NonEmptyString(data["reason"]),
                        is_advance=bool(data["is_advance"]),
                        pay_emitted_id=NonEmptyString(data["specific_id"]),
                        recipient_account=NonEmptyString(data["recipient_account"]),
                    )
                    self.update_emitted_uc.execute(updated_emitted)
                else:
                    updated_received = ReceivedPay(
                        person_id=NonEmptyString(data["person_id"]),
                        pay_id=NonEmptyString(data["pay_id"]),
                        date=NonEmptyString(data["date"]),
                        url=NonEmptyString(url_val),
                        amount=float(data["amount"]),
                        method=NonEmptyString(data["method"]),
                        reason=NonEmptyString(data["reason"]),
                        is_advance=bool(data["is_advance"]),
                        received_pay_id=NonEmptyString(data["specific_id"]),
                        net_amount=float(data["net_amount"]),
                        interest=float(data["interest"]),
                    )
                    self.update_received_uc.execute(updated_received)
                self.load_pays()
            except Exception as e:
                QMessageBox.warning(self.view, "Error de validación", str(e))

    def delete_pay(self, pay: EmittedPay | ReceivedPay):
        confirm = QMessageBox.question(
            self.view,
            "Confirmar eliminación",
            f"¿Estás seguro de eliminar el soporte [{pay.pay_id}]?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                if isinstance(pay, EmittedPay):
                    self.delete_emitted_uc.execute(pay.pay_emitted_id)
                else:
                    self.delete_received_uc.execute(pay.received_pay_id)
                self.load_pays()
            except Exception as e:
                QMessageBox.warning(self.view, "Error al eliminar", str(e))

    def search_pays(self):
        data = self.view.ui.lineEdit.text().strip().lower()
        pays = (
            self.find_all_emitted_uc.execute()
            if self.current_mode == "emitted"
            else self.find_all_received_uc.execute()
        ) or []
        filtered_pays = [
            p for p in pays if any(data in str(v).lower() for v in vars(p).values())
        ]
        self.load_pays(filtered_pays)

    def filter_pays(self):
        methods = ["Todos", "Efectivo", "Transferencia", "Tarjeta", "Nequi/Daviplata"]
        method, ok = QInputDialog.getItem(
            self.view, "Filtrar por método", "Método:", methods, 0, False
        )
        if ok:
            pays = (
                self.find_all_emitted_uc.execute()
                if self.current_mode == "emitted"
                else self.find_all_received_uc.execute()
            ) or []
            if method != "Todos":
                pays = [p for p in pays if str(p.method) == method]
            self.load_pays(pays)
