from pathlib import Path
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication


class ThemeManager:
    @staticmethod
    def apply_artisan_theme(app: QApplication):

        app.setStyle("Fusion")

        palette = QPalette()

        palette.setColor(QPalette.ColorRole.Window, QColor("#F9F6E8"))

        palette.setColor(QPalette.ColorRole.Base, QColor("#FFFFFF"))

        palette.setColor(QPalette.ColorRole.WindowText, QColor("#262115"))

        palette.setColor(QPalette.ColorRole.Text, QColor("#262115"))

        palette.setColor(QPalette.ColorRole.Button, QColor("#6B5724"))

        palette.setColor(QPalette.ColorRole.ButtonText, QColor("#FFFFFF"))

        palette.setColor(QPalette.ColorRole.Highlight, QColor("#C89D3C"))

        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#FFFFFF"))

        app.setPalette(palette)

        qss_path = (
            Path(__file__).resolve().parents[3] / "assets" / "styles" / "artesanal.qss"
        )
        if qss_path.exists():
            app.setStyleSheet(qss_path.read_text(encoding="utf-8"))
