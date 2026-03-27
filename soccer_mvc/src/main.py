from PyQt6.QtWidgets import QApplication
import sys
from src.controller.player_controller import PlayerController
from src.view.windows.main_window import MainWindow


def main():
    controller = PlayerController()

    app = QApplication(sys.argv)
    window = MainWindow(controller)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

