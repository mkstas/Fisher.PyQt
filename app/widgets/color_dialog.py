from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QDialogButtonBox, QMessageBox, QPushButton
)
from PyQt6.QtGui import QColor
import random

class ColorDialog(QDialog):
    __colors = [
        ("#000000", "Чёрный"),
        ("#800000", "Тёмно-красный"),
        ("#008000", "Зелёный"),
        ("#808000", "Оливковый"),
        ("#000080", "Тёмно-синий"),
        ("#800080", "Фиолетовый"),
        ("#008080", "Бирюзовый"),
        ("#c0c0c0", "Серебряный"),
        ("#808080", "Серый"),
        ("#ff0000", "Красный"),
        ("#00ff00", "Лаймовый"),
        ("#ffff00", "Жёлтый"),
        ("#0000ff", "Синий"),
        ("#ff00ff", "Пурпурный"),
        ("#00ffff", "Голубой"),
        ("#ffffff", "Белый")
    ]

    def __init__(self, parent=None, people=None):
        super().__init__(parent)
        
        if people is None:
            people = []
        self.people = people

        self.setWindowTitle("Выбор цвета")
        self.setFixedSize(400, 550)
        
        self.comboboxes = []
        self.current_colors = {}
        self.initial_colors = {}
        self.updated_people = None  # Для хранения обновленных данных
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        if len(self.people) != 10:
            raise ValueError("Количество людей должно быть строго 10")
        
        for person in self.people:
            self.current_colors[person['id']] = person['color']
            self.initial_colors[person['id']] = person['color']
        
        for i, person in enumerate(self.people):
            h_layout = QHBoxLayout()
            
            label = QLabel(f"Человек {person['id']}:")
            combo = QComboBox()
            
            combo.blockSignals(True)
            
            for color_hex, color_name in self.__colors:
                combo.addItem(color_name, color_hex)
            
            current_index = combo.findData(person['color'])
            if current_index >= 0:
                combo.setCurrentIndex(current_index)
            
            combo.blockSignals(False)
            
            combo.currentIndexChanged.connect(
                lambda index, cb=combo, pid=person['id']: self.on_color_changed(cb, pid)
            )
            
            h_layout.addWidget(label)
            h_layout.addWidget(combo)
            layout.addLayout(h_layout)
            self.comboboxes.append(combo)
        
        random_button = QPushButton("СЛУЧАЙНО")
        random_button.clicked.connect(self.randomize_colors)
        layout.addWidget(random_button)
        
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)

    def randomize_colors(self):
        all_colors = [color[0] for color in self.__colors]
        
        if len(all_colors) >= 10:
            selected_colors = random.sample(all_colors, 10)
        else:
            selected_colors = [random.choice(all_colors) for _ in range(10)]
        
        for combo in self.comboboxes:
            combo.blockSignals(True)
        
        for i, combo in enumerate(self.comboboxes):
            color_index = combo.findData(selected_colors[i])
            if color_index >= 0:
                combo.setCurrentIndex(color_index)
                person_id = self.people[i]['id']
                self.current_colors[person_id] = selected_colors[i]
        
        for combo in self.comboboxes:
            combo.blockSignals(False)
        
        QMessageBox.information(
            self,
            "Цвета распределены",
            "Цвета были успешно распределены случайным образом между всеми пользователями."
        )

    def on_color_changed(self, combo, person_id):
        new_color = combo.currentData()
        
        used_by_others = False
        conflicting_person_id = None
        
        for i, other_combo in enumerate(self.comboboxes):
            if other_combo != combo and other_combo.currentData() == new_color:
                used_by_others = True
                conflicting_person_id = self.people[i]['id']
                break
        
        if used_by_others:
            combo.blockSignals(True)
            previous_color = self.current_colors[person_id]
            previous_index = combo.findData(previous_color)
            if previous_index >= 0:
                combo.setCurrentIndex(previous_index)
            combo.blockSignals(False)
            
            QMessageBox.warning(
                self,
                "Цвет уже используется",
                f"Цвет {self.get_color_name(new_color)} уже выбран пользователем {conflicting_person_id}.\n"
                "Пожалуйста, выберите другой цвет."
            )
        else:
            self.current_colors[person_id] = new_color

    def reset_to_initial(self):
        for combo in self.comboboxes:
            combo.blockSignals(True)
        
        for i, person in enumerate(self.people):
            initial_color = self.initial_colors[person['id']]
            initial_index = self.comboboxes[i].findData(initial_color)
            if initial_index >= 0:
                self.comboboxes[i].setCurrentIndex(initial_index)
                self.current_colors[person['id']] = initial_color
        
        for combo in self.comboboxes:
            combo.blockSignals(False)

    def reject(self):
        self.reset_to_initial()
        super().reject()

    def get_color_name(self, color_hex):
        for hex_val, name in self.__colors:
            if hex_val == color_hex:
                return name
        return color_hex

    def get_selected_colors(self):
        return [combo.currentData() for combo in self.comboboxes]

    def get_updated_people(self):
        """Возвращает обновленный список людей с выбранными цветами"""
        updated_people = []
        for i, person in enumerate(self.people):
            updated_person = person.copy()
            updated_person['color'] = self.comboboxes[i].currentData()
            updated_people.append(updated_person)
        return updated_people

    def accept(self):
        # Проверяем, что все цвета уникальны
        colors = [combo.currentData() for combo in self.comboboxes]
        if len(colors) != len(set(colors)):
            QMessageBox.warning(
                self,
                "Дублирование цветов",
                "Некоторые цвета используются несколькими пользователями.\n"
                "Пожалуйста, убедитесь, что у каждого пользователя уникальный цвет."
            )
            return
        
        # Сохраняем обновленные данные
        self.updated_people = self.get_updated_people()
        super().accept()