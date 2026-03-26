from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QHeaderView, QMessageBox
from .ui.dialog_search_ui import Ui_dialog_search
from src.controller.player_controller import PlayerController
from src.model.player import Player
from typing import List


class DialogSearch(QDialog, Ui_dialog_search):
    def __init__(self, controller: PlayerController, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.controller = controller
        self.table_results.setColumnCount(8)
        self.table_results.setHorizontalHeaderLabels(["Фамилия", "Имя", "Отчество", "Дата",
            "Команда", "Город", "Состав", "Позиция"])
        self.table_results.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_results.setEditTriggers(self.table_results.EditTrigger.NoEditTriggers)
        self.input_date.setEnabled(False)
        self.check_date.toggled.connect(self.input_date.setEnabled)
        self.button_search.clicked.connect(self._search)

    def _fill_results(self, players: List[Player]):

        self.label_results.setText(f"Найдено записей {len(players)}")
        self.table_results.setRowCount(len(players))
        for row, player in enumerate(players):
            self.table_results.setItem(row, 0, QTableWidgetItem(player.last_name))
            self.table_results.setItem(row, 1, QTableWidgetItem(player.first_name))
            self.table_results.setItem(row, 2, QTableWidgetItem(player.patronymic or ""))
            self.table_results.setItem(row, 3, QTableWidgetItem(str(player.birth_date)))
            self.table_results.setItem(row, 4, QTableWidgetItem(player.team))
            self.table_results.setItem(row, 5, QTableWidgetItem(player.city))
            self.table_results.setItem(row, 6, QTableWidgetItem(player.squad))
            self.table_results.setItem(row, 7, QTableWidgetItem(player.position))

    def _search(self):
        current_tab = self.tab_widget.currentIndex()
        if current_tab == 0:
            last_name = self.input_last_name.text().strip() or None
            first_name = self.input_first_name.text().strip() or None
            patronymic = self.input_patronymic.text().strip() or None
            birth_date = self.input_date.date().toPyDate() if self.check_date.isChecked() else None
            has_name = any([last_name, first_name, patronymic])
            has_date = birth_date is not None
            if not (has_name and has_date):
                QMessageBox.warning(self, "Ошибка", "Введите имя и дату")
                return
            results = self.controller.search_by_name_date(last_name, first_name, patronymic, birth_date)
        elif current_tab == 1:
            position = self.input_position.text().strip() or None
            squad = self.input_squad.text().strip() or None
            results = self.controller.search_by_position_or_squad(position, squad)
            if not (position or squad):
                QMessageBox.warning(self, "Ошибка", "Введите позицию или состав")
                return
        else:
            team = self.input_team.text().strip() or None
            city = self.input_city.text().strip() or None
            results = self.controller.search_by_team_or_city(team, city)
            if not (team or city):
                QMessageBox.warning(self, "Ошибка", "Введите команду или город")
                return
        self._fill_results(results)
