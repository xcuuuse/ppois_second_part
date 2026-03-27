from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import QDate, Qt
from src.view.ui.dialog_add_ui import Ui_dialog_add
from src.model.player import Player
from src.controller.player_controller import PlayerController


class DialogAdd(QDialog, Ui_dialog_add):
    def __init__(self, controller: PlayerController, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedSize(300, 340) #не хочет чиниться
        self.controller = controller

        self.button_cancel.clicked.connect(self.reject)
        self.button_save.clicked.connect(self._save)

    def _save(self):
        last_name = self.input_last_name.text().strip()
        first_name = self.input_first_name.text().strip()
        patronymic = self.input_patronymic.text().strip() or None
        birth_date = self.input_date.date().toPyDate()
        team = self.input_team.text().strip()
        city = self.input_city.text().strip()
        squad = self.box_squad.currentText() or None
        position = self.box_position.currentText() or None
        if not all([last_name, first_name, team, city, squad, position]):
            QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля")
            return

        player = Player(
            last_name=last_name,
            first_name=first_name,
            patronymic=patronymic,
            birth_date=birth_date,
            team=team,
            city=city,
            squad=squad,
            position=position
        )
        self.controller.add_player_to_database(player)
        self.accept()
