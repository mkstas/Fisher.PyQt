from PyQt6.QtWidgets import (
    QVBoxLayout, QDialog, QVBoxLayout, QLabel, QDialogButtonBox
)
from PyQt6.QtCore import Qt

class AuthorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Об авторе")
        self.setFixedSize(300, 200)
        
        layout = QVBoxLayout()
        
        # Заголовок
        title_label = QLabel("Рыбаки")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        
        # Информация о программе
        info_label = QLabel("Версия 1.0\n\nПриложение для рыболовов")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("margin: 10px;")
        
        # Кнопка OK
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)
        
        layout.addWidget(title_label)
        layout.addWidget(info_label)
        layout.addStretch()
        layout.addWidget(button_box)
        
        self.setLayout(layout)