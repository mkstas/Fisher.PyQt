import random

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QMessageBox, QPushButton
)
from PyQt6.QtGui import QColor, QIcon, QPixmap, QPainter
from PyQt6.QtCore import Qt

class ColorDialog(QDialog):
    __colors = [
        ("#000000", "Чёрный"),
        ("#800000", "Тёмно-красный"),
        ("#008000", "Зелёный"),
        ("#808000", "Оливковый"),
        ("#000080", "Тёмно-синий"),
        ("#800080", "Фиолетовый"),
        ("#008080", "Бирюзовый"),
        ("#c0c0c0", "Светло-серый"),
        ("#808080", "Серый"),
        ("#ff0000", "Красный"),
        ("#00ff00", "Светло-зеленый"),
        ("#ffff00", "Жёлтый"),
        ("#0000ff", "Синий"),
        ("#ff00ff", "Розовый"),
        ("#00ffff", "Голубой"),
        ("#ffffff", "Белый")
    ]

    def __init__(self, parent=None, people=[]):
        super().__init__(parent)

        self.people = people
        self.updated_people = []
        self.comboboxes = []
        self.current_colors = {}
        self.initial_colors = {}

        self.setWindowTitle("Выбор цвета")
        self.setFixedSize(640, 480)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addSpacing(0)
        self.main_layout.setContentsMargins(8, 8, 8, 2)

        self.init_ui()

    def create_color_icon(self, color_hex):
        pixmap = QPixmap(20, 20)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setBrush(QColor("#000000"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, 20, 20, 2, 2)
        painter.setBrush(QColor(color_hex))
        painter.drawRoundedRect(1, 1, 18, 18, 2, 2)

        painter.end()

        return QIcon(pixmap)

    def init_ui(self):
        for person in self.people:
            self.current_colors[person['id']] = person['color']
            self.initial_colors[person['id']] = person['color']

        for i, person in enumerate(self.people):
            h_layout = QHBoxLayout()

            label = QLabel(f"Рыбак {person['id'] + 1}:")
            label.setFixedWidth(100)
            combo = QComboBox()

            combo.setStyleSheet("""
                QComboBox {
                    padding: 6.5px;
                    border: none;
                    border: 1px solid #cbd5e1;
                    border-radius: 4px;
                }
                QComboBox::drop-down {
                    border: none;
                    border-left: 1px solid #cbd5e1;
                }
                QComboBox::down-arrow {
                    image: url(src/resources/chevron-down.svg);
                    width: 16px;
                    height: 16px;
                }
                QComboBox QAbstractItemView {
                    background-color: white;
                    border: 1px solid #cbd5e1;
                    border-radius: 4px;
                    outline: none;
                    selection-color: #000000;
                }
                QComboBox QAbstractItemView::item {
                    padding: 5px 10px;
                    border-top: 1px solid #cbd5e1;
                }
                QComboBox QAbstractItemView::item:hover {
                    color: #000000;
                    background-color: #ede9fe;
                }
            """)

            combo.blockSignals(True)

            # Заполняем комбобокс цветами с иконками
            for color_hex, color_name in self.__colors:
                icon = self.create_color_icon(color_hex)
                combo.addItem(icon, " " + color_name, color_hex)  # Добавляем пробел для отступа

            current_index = combo.findData(person['color'])
            combo.setCurrentIndex(current_index)

            combo.blockSignals(False)

            combo.currentIndexChanged.connect(
                lambda index, cb=combo, pid=person['id']: self.on_color_changed(cb, pid)
            )

            h_layout.addWidget(label)
            h_layout.addWidget(combo)

            self.main_layout.addLayout(h_layout)
            self.comboboxes.append(combo)

        h_layout = QHBoxLayout()

        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)

        random_button = QPushButton("Случайно")
        random_button.clicked.connect(self.randomize_colors)

        ok_button = QPushButton("Ок")
        ok_button.clicked.connect(self.accept)

        h_layout.addWidget(cancel_button)
        h_layout.addWidget(random_button)
        h_layout.addWidget(ok_button)

        self.main_layout.addLayout(h_layout)

    def on_color_changed(self, combo, person_id):
        new_color = combo.currentData()

        is_used = False

        for i, other_combo in enumerate(self.comboboxes):
            if other_combo != combo and other_combo.currentData() == new_color:
                is_used = True
                break

        if is_used:
            combo.blockSignals(True)

            previous_color = self.current_colors[person_id]
            previous_index = combo.findData(previous_color)

            combo.setCurrentIndex(previous_index)
            combo.blockSignals(False)

            QMessageBox.warning(
                self,
                "Цвет уже используется",
                f"Цвет {self.get_color_name(new_color)} уже занят."
            )
        else:
            self.current_colors[person_id] = new_color

    def get_color_name(self, color_hex):
        for hex_val, name in self.__colors:
            if hex_val == color_hex:
                return name
        return color_hex

    def randomize_colors(self):
        available_colors = [color[0] for color in self.__colors]        
        random.shuffle(available_colors)
        selected_colors = available_colors[:len(self.comboboxes)]

        for combo in self.comboboxes:
            combo.blockSignals(True)

        for i, combo in enumerate(self.comboboxes):
            color_hex = selected_colors[i]
            color_index = combo.findData(color_hex)
            if color_index >= 0:
                combo.setCurrentIndex(color_index)
                person_id = self.people[i]['id']
                self.current_colors[person_id] = color_hex

        for combo in self.comboboxes:
            combo.blockSignals(False)

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

    def get_updated_people(self):
        updated_people = []
        for i, person in enumerate(self.people):
            updated_person = person.copy()
            updated_person['color'] = self.comboboxes[i].currentData()
            updated_people.append(updated_person)
        return updated_people

    def accept(self):
        self.updated_people = self.get_updated_people()
        super().accept()
