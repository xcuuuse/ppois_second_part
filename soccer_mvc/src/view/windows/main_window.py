from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QTreeWidgetItem, QDialog, QFileDialog
from src.view.ui.main_window_ui import Ui_Players
from src.controller.player_controller import PlayerController
from src.view.windows.dialog_add import DialogAdd
from src.view.windows.dialog_delete import DialogDelete
from src.view.windows.paginator import Paginator
from src.view.windows.dialog_search import DialogSearch


class MainWindow(QMainWindow, Ui_Players):
    def __init__(self, controller: PlayerController):
        super().__init__()
        self.setupUi(self)
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Фамилия", "Имя", "Отчество", "Дата",
            "Команда", "Город", "Состав", "Позиция"
        ])
        self.controller = controller
        self.button_tree_view.clicked.connect(self._tree_table_swap)
        self.button_add.clicked.connect(self._add_dialog)
        self.paginator = Paginator(self.controller, self.refresh, parent=self)
        self.verticalLayout.addWidget(self.paginator)
        self.button_search.clicked.connect(self._dialog_search)
        self.button_remove.clicked.connect(self._dialog_delete)
        self.button_save_to_xml.clicked.connect(self._save_to_xml)
        self.button_load_from_xml.clicked.connect(self._load_from_xml)
        self.refresh()

    def _fill_table(self, players):
        self.table.clearContents()
        self.table.setRowCount(len(players))
        for row, player in enumerate(players):
            self.table.setItem(row, 0, QTableWidgetItem(player.last_name))
            self.table.setItem(row, 1, QTableWidgetItem(player.first_name))
            self.table.setItem(row, 2, QTableWidgetItem(player.patronymic or ""))
            self.table.setItem(row, 3, QTableWidgetItem(str(player.birth_date)))
            self.table.setItem(row, 4, QTableWidgetItem(player.team))
            self.table.setItem(row, 5, QTableWidgetItem(player.city))
            self.table.setItem(row, 6, QTableWidgetItem(player.squad))
            self.table.setItem(row, 7, QTableWidgetItem(player.position))

    def _fill_tree(self, players):
        self.tree.clear()
        for player in players:
            root = QTreeWidgetItem(self.tree, [f"{player.last_name} {player.first_name}"])
            QTreeWidgetItem(root, [f"Отчество: {player.patronymic or '-'}"])
            QTreeWidgetItem(root, [f"Дата рождения: {player.birth_date}"])
            QTreeWidgetItem(root, [f"Команда: {player.team}"])
            QTreeWidgetItem(root, [f"Город: {player.city}"])
            QTreeWidgetItem(root, [f"Состав: {player.squad}"])
            QTreeWidgetItem(root, [f"Позиция: {player.position}"])

    def _add_dialog(self):
        dialog = DialogAdd(self.controller, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh()

    def _tree_table_swap(self):
        if self.stacked_widget.currentIndex() == 0:
            self.stacked_widget.setCurrentIndex(1)
            self.button_tree_view.setText("Показать таблицу")
        else:
            self.stacked_widget.setCurrentIndex(0)
            self.button_tree_view.setText("Показать дерево")

    def _dialog_search(self):
        dialog = DialogSearch(self.controller, parent=self)
        dialog.exec()

    def _dialog_delete(self):
        dialog = DialogDelete(self.controller, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh()

    def _save_to_xml(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Сохранить в XML", "", "XML Files (*.xml)")
        if filename:
            self.controller.save_to_xml(filename)

    def _load_from_xml(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Загрузить из XML", "", "XML Files (*.xml)")
        if filename:
            self.controller.read_from_xml(filename)
            self.refresh()

    def refresh(self):
        players, current_page, total_pages, total = self.controller.get_current_page()
        self._fill_table(players)
        self._fill_tree(players)
        self.paginator.update_info(current_page, total_pages)
