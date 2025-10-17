from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, 
    QMessageBox, QPushButton
)

class InitialDialog(QDialog):
    def __init__(self, parent=None, people=[]):
        super().__init__(parent)

        self.people = people
        self.original_people = people
        self.spinboxes = []

        self.setWindowTitle("Начальное заполнение")
        self.setFixedSize(640, 480)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addSpacing(0)
        self.main_layout.setContentsMargins(8, 8, 8, 2)

        self.init_ui()

    def init_ui(self):
        for i, person in enumerate(self.people):
            h_layout = QHBoxLayout()

            label = QLabel(f"Рыбак {person['id'] + 1}:")
            label.setFixedWidth(100)
            spinbox = QSpinBox()

            spinbox.setRange(0, 9)
            spinbox.setValue(person["count"])
            spinbox.person_id = person["id"]

            h_layout.addWidget(label)
            h_layout.addWidget(spinbox)

            self.main_layout.addLayout(h_layout)
            self.spinboxes.append(spinbox)
