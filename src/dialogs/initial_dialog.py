from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton
)
from PyQt6.QtGui import QIntValidator

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
            
            validator = QIntValidator(0, 9, self)
            spinbox.lineEdit().setValidator(validator)
            
            spinbox.lineEdit().textChanged.connect(
                lambda text, sb=spinbox: self.prevent_leading_zeros(sb, text)
            )
            spinbox.editingFinished.connect(
                lambda sb=spinbox: self.final_validation(sb)
            )

            h_layout.addWidget(label)
            h_layout.addWidget(spinbox)

            self.main_layout.addLayout(h_layout)
            self.spinboxes.append(spinbox)

        h_layout = QHBoxLayout()

        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)

        clear_button = QPushButton("Очистить")
        clear_button.clicked.connect(self.clear_all)

        ok_button = QPushButton("Ок")
        ok_button.clicked.connect(self.accept)

        h_layout.addWidget(cancel_button)
        h_layout.addWidget(clear_button)
        h_layout.addWidget(ok_button)

        self.main_layout.addLayout(h_layout)

    def prevent_leading_zeros(self, spinbox, text):
        if text and len(text) > 1 and text.startswith('0'):
            clean_text = text.lstrip('0') or '0'
            spinbox.lineEdit().setText(clean_text)

    def final_validation(self, spinbox):
        text = spinbox.lineEdit().text()
        if text and text.startswith('0') and len(text) > 1:
            clean_text = text.lstrip('0') or '0'
            try:
                value = int(clean_text)
                spinbox.setValue(min(max(value, spinbox.minimum()), spinbox.maximum()))
            except ValueError:
                spinbox.setValue(0)

    def clear_all(self):
        for spinbox in self.spinboxes:
            spinbox.setValue(0)

    def accept(self):
        self.update_people_data()
        super().accept()

    def reject(self):
        self.restore_original_values()
        super().reject()

    def update_people_data(self):
        for spinbox in self.spinboxes:
            for person in self.people:
                if person["id"] == spinbox.person_id:
                    person["count"] = spinbox.value()
                    break

    def restore_original_values(self):
        for spinbox in self.spinboxes:
            for person in self.original_people:
                if person["id"] == spinbox.person_id:
                    spinbox.setValue(person["count"])
                    break
        
        self.people = self.original_people

    def get_updated_people(self):
        return self.people
