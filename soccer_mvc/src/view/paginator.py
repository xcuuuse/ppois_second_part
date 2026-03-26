from PyQt6.QtWidgets import QWidget
from .ui.paginator_ui import Ui_Paginator
from src.controller.player_controller import PlayerController


class Paginator(QWidget, Ui_Paginator):
    def __init__(self, controller: PlayerController, refresh, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.controller = controller
        self.refresh = refresh
        self.combo_per_page.addItems(["3", "5", "10", "20"])
        self.combo_per_page.setCurrentText("5")
        self.button_first.clicked.connect(self._first)
        self.button_last.clicked.connect(self._last)
        self.button_next.clicked.connect(self._next)
        self.button_previous.clicked.connect(self._previous)
        self.combo_per_page.currentTextChanged.connect(self._change_per_page)
        self.controller.players_per_page(int(self.combo_per_page.currentText()))

    def update_info(self, current_page, total_pages):
        self.label_page_info.setText(
            f"Страница {current_page} из {total_pages}"
        )

    def _notify(self):
        self.refresh()

    def _first(self):
        self.controller.first_page()
        self._notify()

    def _last(self):
        self.controller.last_page()
        self._notify()

    def _next(self):
        self.controller.next_page()
        self._notify()

    def _previous(self):
        self.controller.previous_page()
        self._notify()

    def _change_per_page(self, value: int):
        self.controller.players_per_page(int(value))
        self._notify()







