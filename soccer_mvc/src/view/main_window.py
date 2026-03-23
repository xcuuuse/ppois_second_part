from PyQt6.QtWidgets import \
    (QMainWindow,
     QWidget,
     QVBoxLayout,
     QHBoxLayout,
     QPushButton,
     QStackedWidget,
     QTableWidget,
     QTreeWidget,
     QTableWidgetItem,
     QTreeWidgetItem,
     QHeaderView)
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Soccer Players")
        self.resize(1000, 600)
        central_wiget = QWidget()
        self.setCentralWidget(central_wiget)
        self.main_layout = QVBoxLayout()
        central_wiget.setLayout(self.main_layout)
        self._init_buttons()
        self._init_view_area()
        self.button_tree_view.clicked.connect(self._tree_table_swap)
        self.refresh()

    def _init_buttons(self):
        button_layout = QHBoxLayout()
        self.button_add = QPushButton("Добавить")
        self.button_search = QPushButton("Поиск")
        self.button_delete = QPushButton("Удалить")
        self.button_save_xml = QPushButton("Сохранить в XML")
        self.button_load_xml = QPushButton("Загрузить из XML")
        self.button_tree_view = QPushButton("Показать дерево")

        for button in [
            self.button_add,
            self.button_search,
            self.button_delete,
            self.button_save_xml,
            self.button_load_xml,
            self.button_tree_view
        ]:
            button_layout.addWidget(button)
        self.main_layout.addLayout(button_layout)

    def _init_view_area(self):
        self.stacked_widget = QStackedWidget()
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ["Фамилия", "Имя", "Отчество", "Дата", "Команда", "Город", "Состав", "Позиция"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Игроки")
        self.stacked_widget.addWidget(self.table)
        self.stacked_widget.addWidget(self.tree)
        self.main_layout.addWidget(self.stacked_widget)

    def _fill_table(self, players):
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

    def _tree_table_swap(self):
        if self.stacked_widget.currentIndex() == 0:
            self.stacked_widget.setCurrentIndex(1)
            self.button_tree_view.setText("Показать таблицу")
        else:
            self.stacked_widget.setCurrentIndex(0)
            self.button_tree_view.setText("Показать дерево")

    def refresh(self):
        players, current_page, total_pages, total = self.controller.get_current_page()
        self._fill_table(players)
        self._fill_tree(players)
