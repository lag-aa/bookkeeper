from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QDialog


class BudgetWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(QLabel("Budget Widget"))

        btn = QPushButton("Клик")
        layout.addWidget(btn)
        btn.clicked.connect(self.button_clicked)
        # Здесь вы можете добавить элементы управления для отображения бюджета на день/неделю/месяц и функциональность для редактирования

    def button_clicked(self, s):
        dlg = QDialog(self)
        dlg.setWindowTitle("QDialog")
        dlg.resize(200, 50)
        dlg.exec()
