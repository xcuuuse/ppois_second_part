from src.view.ui.dialog_delete_ui import Ui_DialogDelete
from PyQt6.QtWidgets import QDialog, QMessageBox
from src.controller.player_controller import PlayerController


class DialogDelete(QDialog, Ui_DialogDelete):
    def __init__(self, controller: PlayerController, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.controller = controller
        self.date_box.toggled.connect(self.input_date.setEnabled)
        self.button_delete.clicked.connect(self._delete)
        self.setFixedSize(521, 354)

    def _delete(self):
        current_tab = self.tab_widget.currentIndex()
        amount = self.controller.get_total()
        if current_tab == 0:
            last_name = self.input_last_name.text().strip() or None
            first_name = self.input_first_name.text().strip() or None
            patronymic = self.input_patronymic.text().strip() or None
            birth_date = self.input_date.date().toPyDate() if self.date_box.isChecked() else None
            has_name = any([last_name, first_name, patronymic])
            has_date = birth_date is not None
            if not (has_name and has_date):
                QMessageBox.warning(self, "Ошибка", "Введите имя или дату")
                return
            self.controller.delete_by_name_date(last_name, first_name, patronymic, birth_date)
        elif current_tab == 1:
            position = self.box_position.currentText() or None
            squad = self.box_squad.currentText() or None
            if not (position or squad):
                QMessageBox.warning(self, "Ошибка", "Введите позицию или состав")
                return
            self.controller.delete_by_position_or_squad(position, squad)
        else:
            team = self.team_edit.text().strip() or None
            city = self.city_edit.text().strip() or None
            if not (team or city):
                QMessageBox.warning(self, "Ошибка", "Введите команду или город")
                return
            self.controller.delete_by_team_or_city(team, city)
        self.accept()
        QMessageBox.information(self, "Удаление", f"Удалено записей: {amount - self.controller.get_total()}")
