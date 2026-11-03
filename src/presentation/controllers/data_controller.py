import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtGui import QPdfWriter, QStandardItem, QStandardItemModel, QTextDocument
from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QListView,
    QMessageBox,
    QVBoxLayout,
)
from ui.views.data_view import DataView
from src.application.services.find_all_products_use_case import FindAllProductsUseCase
from src.application.services.find_all_person_use_case import FindAllPersonUseCase
from src.application.services.find_all_emitted_pay_use_case import (
    FindAllEmittedPayUseCase,
)
from src.application.services.find_all_received_pay_use_case import (
    FindAllReceivedPayUseCase,
)


class DataController:
    def __init__(
        self,
        view: DataView,
        find_products_uc: FindAllProductsUseCase,
        find_persons_uc: FindAllPersonUseCase,
        find_emitted_uc: FindAllEmittedPayUseCase,
        find_received_uc: FindAllReceivedPayUseCase,
    ):
        self.view = view
        self.find_products_uc = find_products_uc
        self.find_persons_uc = find_persons_uc
        self.find_emitted_uc = find_emitted_uc
        self.find_received_uc = find_received_uc

        self.kpi_labels: list[QLabel] = []
        for w in (
            self.view.ui.widget_2,
            self.view.ui.widget_3,
            self.view.ui.widget_4,
            self.view.ui.widget_5,
        ):
            layout = QVBoxLayout(w)
            lbl = QLabel()
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setWordWrap(True)
            lbl.setStyleSheet(
                "font-size: 14px; font-weight: bold; padding: 8px; border: 1px solid #6B5724; border-radius: 8px;"
            )
            layout.addWidget(lbl)
            self.kpi_labels.append(lbl)

        left_layout = QVBoxLayout(self.view.ui.widget_6)
        left_title = QLabel("Registros Analizados (Pandas)")
        left_title.setStyleSheet("font-weight: bold;")
        self.detail_list = QListView()
        self.detail_model = QStandardItemModel()
        self.detail_list.setModel(self.detail_model)
        left_layout.addWidget(left_title)
        left_layout.addWidget(self.detail_list)

        right_layout = QVBoxLayout(self.view.ui.widget_7)
        self.summary_label = QLabel()
        self.summary_label.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.summary_label.setWordWrap(True)
        self.summary_label.setStyleSheet(
            "padding: 10px; border: 1px solid #6B5724; border-radius: 8px;"
        )
        right_layout.addWidget(self.summary_label)

        self.view.ui.pushButton_7.clicked.connect(self.refresh_analytics)
        self.view.ui.comboBox.currentTextChanged.connect(self.refresh_analytics)
        self.view.ui.lineEdit.textChanged.connect(self.refresh_analytics)
        self.view.ui.pushButton_9.clicked.connect(self.export_data)
        self.view.ui.pushButton_8.clicked.connect(self.import_data)

        self.refresh_analytics()

    def _build_dataframes(self) -> dict[str, pd.DataFrame]:
        products = self.find_products_uc.execute() or []
        persons = self.find_persons_uc.execute() or []
        emitted = self.find_emitted_uc.execute() or []
        received = self.find_received_uc.execute() or []

        df_prod = pd.DataFrame(
            [
                {
                    "ID": str(p.product_id),
                    "Nombre": str(p.name),
                    "Precio": float(p.price),
                    "Estado": str(p.state),
                }
                for p in products
            ]
        )
        df_pers = pd.DataFrame(
            [
                {
                    "ID": str(p.person_id),
                    "Nombre": str(p.name),
                    "Rol": str(p.role),
                    "Email": str(p.email),
                }
                for p in persons
            ]
        )
        df_comp = pd.DataFrame(
            [
                {
                    "ID": str(p.pay_emitted_id),
                    "Tercero": str(p.person_id),
                    "Fecha": str(p.date),
                    "Monto": float(p.amount),
                    "Método": str(p.method),
                }
                for p in emitted
            ]
        )
        df_vent = pd.DataFrame(
            [
                {
                    "ID": str(p.received_pay_id),
                    "Tercero": str(p.person_id),
                    "Fecha": str(p.date),
                    "Neto": float(p.net_amount or p.amount),
                    "Interés": float(p.interest),
                }
                for p in received
            ]
        )
        return {
            "Inventario": df_prod,
            "Terceros": df_pers,
            "Compras": df_comp,
            "Ventas": df_vent,
        }

    def refresh_analytics(self):
        dfs = self._build_dataframes()
        df_prod = dfs["Inventario"]
        df_pers = dfs["Terceros"]
        df_comp = dfs["Compras"]
        df_vent = dfs["Ventas"]

        total_inv = df_prod["Precio"].sum() if not df_prod.empty else 0.0
        total_comp = df_comp["Monto"].sum() if not df_comp.empty else 0.0
        total_vent = df_vent["Neto"].sum() if not df_vent.empty else 0.0

        self.kpi_labels[0].setText(
            f"Inventario\n{len(df_prod)} prods\nValor: ${total_inv:,.2f}"
        )
        self.kpi_labels[1].setText(f"Terceros\n{len(df_pers)} registrados")
        self.kpi_labels[2].setText(
            f"Compras\n{len(df_comp)} soportes\n${total_comp:,.2f}"
        )
        self.kpi_labels[3].setText(
            f"Ventas\n{len(df_vent)} soportes\n${total_vent:,.2f}"
        )

        area = self.view.ui.comboBox.currentText()
        query = self.view.ui.lineEdit.text().strip().lower()

        selected_areas = (
            [area]
            if area in dfs
            else ["Inventario", "Terceros", "Compras", "Ventas"]
        )

        self.detail_model.clear()
        for a in selected_areas:
            df = dfs[a]
            if df.empty:
                continue
            for _, row in df.iterrows():
                row_text = f"[{a}] " + " | ".join(f"{k}: {v}" for k, v in row.items())
                if not query or query in row_text.lower():
                    item = QStandardItem(row_text)
                    item.setEditable(False)
                    self.detail_model.appendRow(item)

        balance = total_vent - total_comp
        prom_prod = df_prod["Precio"].mean() if not df_prod.empty else 0.0
        self.summary_label.setText(
            f"RESUMEN EJECUTIVO\n\n"
            f"Área activa: {area}\n"
            f"Balance (Ventas - Compras): ${balance:,.2f}\n"
            f"Precio promedio artesanía: ${prom_prod:,.2f}\n"
            f"Total terceros activos: {len(df_pers)}\n"
            f"Total movimientos: {len(df_comp) + len(df_vent)}"
        )

    def export_data(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self.view,
            "Exportar Reporte General",
            "reporte_tienda.csv",
            "CSV (*.csv);;Excel (*.xlsx);;PDF (*.pdf)",
        )
        if not file_path:
            return
        try:
            dfs = self._build_dataframes()
            area = self.view.ui.comboBox.currentText()
            target_df = (
                dfs[area]
                if area in dfs
                else pd.concat(
                    [df.assign(Area=k) for k, df in dfs.items() if not df.empty],
                    ignore_index=True,
                )
            )
            if file_path.endswith(".xlsx"):
                try:
                    target_df.to_excel(file_path, index=False)
                except ImportError:
                    file_path = file_path.replace(".xlsx", ".csv")
                    target_df.to_csv(file_path, index=False)
            elif file_path.endswith(".pdf"):
                writer = QPdfWriter(file_path)
                doc = QTextDocument()
                doc.setHtml(
                    f"<h2>Reporte Analítico ({area})</h2>"
                    + target_df.to_html(index=False)
                )
                doc.print_(writer)
            else:
                target_df.to_csv(file_path, index=False)
            QMessageBox.information(
                self.view, "Exportación exitosa", f"Datos exportados en:\n{file_path}"
            )
        except Exception as e:
            QMessageBox.warning(self.view, "Error al exportar", str(e))

    def import_data(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.view,
            "Importar Datos para Análisis (CSV / Excel)",
            "",
            "Archivos de datos (*.csv *.xlsx)",
        )
        if not file_path:
            return
        try:
            df = (
                pd.read_excel(file_path)
                if file_path.endswith(".xlsx")
                else pd.read_csv(file_path)
            )
            self.detail_model.clear()
            for _, row in df.iterrows():
                txt = "[Importado] " + " | ".join(f"{k}: {v}" for k, v in row.items())
                item = QStandardItem(txt)
                item.setEditable(False)
                self.detail_model.appendRow(item)
            QMessageBox.information(
                self.view,
                "Importación exitosa",
                f"Se cargaron {len(df)} filas con Pandas.",
            )
        except Exception as e:
            QMessageBox.warning(self.view, "Error al importar", str(e))
