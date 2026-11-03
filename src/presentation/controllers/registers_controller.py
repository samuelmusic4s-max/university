from pathlib import Path
import pandas as pd
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import (
    QIcon,
    QImage,
    QPainter,
    QPdfWriter,
    QPixmap,
    QStandardItem,
    QStandardItemModel,
    QTextDocument,
)
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QListView,
    QMessageBox,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)
from ui.views.registers_view import RegistersView
from ui.views.pay_dialog import PayDialog
from src.domain.entities.emitted_pay import EmittedPay
from src.domain.entities.received_pay import ReceivedPay
from src.domain.value_objects.non_empty_string import NonEmptyString
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


class RegistersController:
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
        self.current_preview_path = ""

        self.metrics_model = QStandardItemModel()
        self.view.ui.listView.setModel(self.metrics_model)
        self.view.ui.listView.setFlow(QListView.Flow.LeftToRight)
        self.view.ui.listView.setSpacing(10)

        self.list_model = QStandardItemModel()
        self.view.ui.listView_2.setModel(self.list_model)
        self.view.ui.listView_2.setIconSize(QSize(48, 48))

        preview_layout = QVBoxLayout(self.view.ui.widget_2)
        self.preview_lbl = QLabel("Seleccione un soporte")
        self.preview_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setMinimum(80)
        self.zoom_slider.setMaximum(320)
        self.zoom_slider.setValue(180)
        self.zoom_slider.valueChanged.connect(self.update_preview_zoom)
        preview_layout.addWidget(self.preview_lbl)
        preview_layout.addWidget(QLabel("Zoom:"))
        preview_layout.addWidget(self.zoom_slider)

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

    def update_metrics(self):
        emitted = self.find_all_emitted_uc.execute() or []
        received = self.find_all_received_uc.execute() or []
        total_compras = sum(p.amount for p in emitted)
        total_ventas = sum(
            (p.net_amount if p.net_amount is not None else p.amount) for p in received
        )
        balance = total_ventas - total_compras

        self.metrics_model.clear()
        cards = [
            f"Total Compras\n${total_compras:,.2f} ({len(emitted)})",
            f"Total Ventas\n${total_ventas:,.2f} ({len(received)})",
            f"Balance Neto\n${balance:,.2f}",
            f"Total Soportes\n{len(emitted) + len(received)} docs",
        ]
        for text in cards:
            item = QStandardItem(text)
            item.setEditable(False)
            item.setSizeHint(QSize(165, 70))
            self.metrics_model.appendRow(item)

    def show_preview(self, path: str):
        self.current_preview_path = path
        self.update_preview_zoom()

    def update_preview_zoom(self):
        if not self.current_preview_path:
            return
        pixmap = QPixmap(self.current_preview_path)
        if not pixmap.isNull():
            size = self.zoom_slider.value()
            self.preview_lbl.setPixmap(
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

    def open_add_dialog(self):
        dialog = PayDialog(mode=self.current_mode, parent=self.view)
        if dialog.exec():
            data = dialog.get_data()
            try:
                if not data["url"]:
                    data["url"] = self.generate_receipt_files(data, self.current_mode)
                if self.current_mode == "emitted":
                    pay = EmittedPay(
                        person_id=NonEmptyString(data["person_id"]),
                        pay_id=NonEmptyString(data["pay_id"]),
                        date=NonEmptyString(data["date"]),
                        url=NonEmptyString(data["url"]),
                        amount=float(data["amount"]),
                        method=NonEmptyString(data["method"]),
                        reason=NonEmptyString(data["reason"]),
                        is_advance=bool(data["is_advance"]),
                        pay_emitted_id=NonEmptyString(data["specific_id"]),
                        recipient_account=NonEmptyString(data["recipient_account"]),
                    )
                    self.save_emitted_uc.execute(pay)
                else:
                    pay = ReceivedPay(
                        person_id=NonEmptyString(data["person_id"]),
                        pay_id=NonEmptyString(data["pay_id"]),
                        date=NonEmptyString(data["date"]),
                        url=NonEmptyString(data["url"]),
                        amount=float(data["amount"]),
                        method=NonEmptyString(data["method"]),
                        reason=NonEmptyString(data["reason"]),
                        is_advance=bool(data["is_advance"]),
                        received_pay_id=NonEmptyString(data["specific_id"]),
                        net_amount=float(data["net_amount"]),
                        interest=float(data["interest"]),
                    )
                    self.save_received_uc.execute(pay)
                self.load_pays()
            except Exception as e:
                QMessageBox.warning(self.view, "Error de validación", str(e))

    def load_pays(self, pays: list | None = None):
        self.update_metrics()
        if pays is None:
            if self.current_mode == "emitted":
                pays = self.find_all_emitted_uc.execute() or []
            else:
                pays = self.find_all_received_uc.execute() or []

        self.list_model.clear()
        for pay in pays:
            if isinstance(pay, EmittedPay):
                txt = f"[Compra {pay.pay_emitted_id}] ${pay.amount:,.2f} - Tercero: {pay.person_id}\n{pay.date} | {pay.method} | {pay.reason}"
            else:
                txt = f"[Venta {pay.received_pay_id}] Neto: ${pay.net_amount:,.2f} (Int: {pay.interest}%)\n{pay.date} | Tercero: {pay.person_id} | {pay.reason}"

            item = QStandardItem(txt)
            item.setEditable(False)
            item.setSizeHint(QSize(0, 75))
            item.setIcon(QIcon(str(pay.url)))
            self.list_model.appendRow(item)
            index = self.list_model.indexFromItem(item)

            row_widget = QWidget()
            row_widget.setStyleSheet("background-color: transparent;")
            item_layout = QHBoxLayout(row_widget)
            item_layout.setContentsMargins(0, 0, 8, 0)
            item_layout.addStretch()

            ver_btn = QPushButton("Ver")
            pdf_btn = QPushButton("Exportar")
            edit_btn = QPushButton("Editar")
            del_btn = QPushButton("Eliminar")

            ver_btn.clicked.connect(
                lambda checked=False, p=pay: self.show_preview(str(p.url))
            )
            pdf_btn.clicked.connect(lambda checked=False, p=pay: self.export_pay(p))
            edit_btn.setStyleSheet("background-color: #6B5724; color: #FFFFFF;")
            edit_btn.clicked.connect(
                lambda checked=False, p=pay: self.open_edit_dialog(p)
            )
            del_btn.setStyleSheet("background-color: #C62828; color: #FFFFFF;")
            del_btn.clicked.connect(lambda checked=False, p=pay: self.delete_pay(p))

            item_layout.addWidget(ver_btn)
            item_layout.addWidget(pdf_btn)
            item_layout.addWidget(edit_btn)
            item_layout.addWidget(del_btn)
            self.view.ui.listView_2.setIndexWidget(index, row_widget)

    def export_pay(self, pay: EmittedPay | ReceivedPay):
        file_path, _ = QFileDialog.getSaveFileName(
            self.view,
            "Exportar Comprobante (PDF, CSV o Excel)",
            f"comprobante_{pay.pay_id}.pdf",
            "PDF (*.pdf);;CSV (*.csv);;Excel (*.xlsx)",
        )
        if not file_path:
            return
        try:
            row = {k: str(v) for k, v in vars(pay).items()}
            if file_path.endswith(".xlsx"):
                try:
                    pd.DataFrame([row]).to_excel(file_path, index=False)
                except ImportError:
                    csv_fallback = file_path.replace(".xlsx", ".csv")
                    pd.DataFrame([row]).to_csv(csv_fallback, index=False)
                    file_path = csv_fallback
            elif file_path.endswith(".csv"):
                pd.DataFrame([row]).to_csv(file_path, index=False)
            else:
                writer = QPdfWriter(file_path)
                doc = QTextDocument()
                html = "<h2>Comprobante de Pago</h2><hr/>" + "".join(
                    f"<p><b>{k}:</b> {v}</p>" for k, v in row.items()
                )
                doc.setHtml(html)
                doc.print_(writer)
            QMessageBox.information(
                self.view, "Exportado", f"Comprobante guardado en:\n{file_path}"
            )
        except Exception as e:
            QMessageBox.warning(self.view, "Error al exportar", str(e))

    def open_edit_dialog(self, pay: EmittedPay | ReceivedPay):
        dialog = PayDialog(mode=self.current_mode, pay=pay, parent=self.view)
        if dialog.exec():
            data = dialog.get_data()
            try:
                if not data["url"]:
                    data["url"] = self.generate_receipt_files(data, self.current_mode)
                if self.current_mode == "emitted":
                    updated = EmittedPay(
                        person_id=NonEmptyString(data["person_id"]),
                        pay_id=NonEmptyString(data["pay_id"]),
                        date=NonEmptyString(data["date"]),
                        url=NonEmptyString(data["url"]),
                        amount=float(data["amount"]),
                        method=NonEmptyString(data["method"]),
                        reason=NonEmptyString(data["reason"]),
                        is_advance=bool(data["is_advance"]),
                        pay_emitted_id=NonEmptyString(data["specific_id"]),
                        recipient_account=NonEmptyString(data["recipient_account"]),
                    )
                    self.update_emitted_uc.execute(updated)
                else:
                    updated = ReceivedPay(
                        person_id=NonEmptyString(data["person_id"]),
                        pay_id=NonEmptyString(data["pay_id"]),
                        date=NonEmptyString(data["date"]),
                        url=NonEmptyString(data["url"]),
                        amount=float(data["amount"]),
                        method=NonEmptyString(data["method"]),
                        reason=NonEmptyString(data["reason"]),
                        is_advance=bool(data["is_advance"]),
                        received_pay_id=NonEmptyString(data["specific_id"]),
                        net_amount=float(data["net_amount"]),
                        interest=float(data["interest"]),
                    )
                    self.update_received_uc.execute(updated)
                self.load_pays()
            except Exception as e:
                QMessageBox.warning(self.view, "Error al editar", str(e))

    def delete_pay(self, pay: EmittedPay | ReceivedPay):
        confirm = QMessageBox.question(
            self.view,
            "Confirmar eliminación",
            f"¿Eliminar soporte {pay.pay_id}?",
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
        q = self.view.ui.lineEdit.text().strip().lower()
        pays = (
            self.find_all_emitted_uc.execute()
            if self.current_mode == "emitted"
            else self.find_all_received_uc.execute()
        ) or []
        filtered = [
            p for p in pays if any(q in str(v).lower() for v in vars(p).values())
        ]
        self.load_pays(filtered)

    def filter_pays(self):
        methods = ["Todos", "Efectivo", "Transferencia", "Tarjeta", "Nequi/Daviplata"]
        method, ok = QInputDialog.getItem(
            self.view, "Filtrar por Método", "Método:", methods, 0, False
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
