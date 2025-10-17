from PyQt6.QtWidgets import (
    QVBoxLayout, QDialog, QLabel, QDialogButtonBox, QSpinBox, 
    QGridLayout, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt
import copy

class InitialDialog(QDialog):
    def __init__(self, people, parent=None):
        super().__init__(parent)
        # Сохраняем копию исходных данных
        self.original_people = copy.deepcopy(people)
        self.people = people
        self.spinboxes = []
        
        self.setWindowTitle("Начальное заполнение")
        self.setFixedSize(300, 400)

        layout = QVBoxLayout()
        grid_layout = QGridLayout()

        # Создаем и настраиваем числовые поля ввода
        for i, person in enumerate(self.people):
            label = QLabel(f"Человек {person['id']}:")
            spinbox = QSpinBox()
            
            # Устанавливаем диапазон от 0 до 9
            spinbox.setRange(0, 9)
            
            # Устанавливаем текущее значение из данных
            spinbox.setValue(person["count"])
            
            # Сохраняем ссылку на спин-бокс и исходные данные
            spinbox.person_id = person["id"]
            self.spinboxes.append(spinbox)
            
            # Добавляем в сетку (2 колонки)
            row = i // 2
            col = i % 2
            grid_layout.addWidget(label, row, col*2)
            grid_layout.addWidget(spinbox, row, col*2 + 1)

        layout.addLayout(grid_layout)

        # Создаем кнопку "Очистить"
        clear_button = QPushButton("Очистить")
        clear_button.clicked.connect(self.clear_all)
        
        # Создаем кнопки диалога
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # Создаем горизонтальный layout для кнопок
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(clear_button)
        buttons_layout.addWidget(button_box)
        
        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def clear_all(self):
        """Устанавливает все значения в 0"""
        for spinbox in self.spinboxes:
            spinbox.setValue(0)

    def accept(self):
        """Сохраняет значения при нажатии OK"""
        self.update_people_data()
        super().accept()

    def reject(self):
        """Восстанавливает исходные значения при нажатии Cancel"""
        self.restore_original_values()
        super().reject()

    def update_people_data(self):
        """Обновляет массив people текущими значениями из спинбоксов"""
        for spinbox in self.spinboxes:
            for person in self.people:
                if person["id"] == spinbox.person_id:
                    person["count"] = spinbox.value()
                    break

    def restore_original_values(self):
        """Восстанавливает исходные значения в спинбоксах и данных"""
        for spinbox in self.spinboxes:
            for person in self.original_people:
                if person["id"] == spinbox.person_id:
                    spinbox.setValue(person["count"])
                    break
        
        # Восстанавливаем исходные данные
        self.people.clear()
        self.people.extend(copy.deepcopy(self.original_people))

    def get_updated_people(self):
        """Возвращает обновленный массив people после редактирования"""
        return self.people