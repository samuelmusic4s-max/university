import sys
from PySide6.QtWidgets import QApplication
from ui.views.main_window import MainWindow
from src.presentation.utils.theme_manager import ThemeManager
from src.infrastructure.db.db_connection import init_db

from src.presentation.controllers.app_handler import AppHandler


def main():

    init_db()

    app = QApplication(sys.argv)

    ThemeManager.apply_artisan_theme(app)

    window = MainWindow()
    app_handler = AppHandler(window)

    window.setWindowTitle("Administrador Tienda Artesanias")
    window.resize(1000, 650)

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
