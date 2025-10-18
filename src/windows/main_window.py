import json
import random

from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QDialog, QFileDialog,
    QLineEdit, QSlider, QPushButton, QMessageBox, QLabel
)
from PyQt6.QtGui import QAction
from dialogs.author_dialog import AuthorDialog
from dialogs.about_dialog import AboutDialog
from dialogs.color_dialog import ColorDialog
from dialogs.initial_dialog import InitialDialog
from widgets.fisher import Fisher

class MainWindow(QMainWindow):
    speed = 0
    alarm = 0
    game_timer = None
    is_running = False
    is_paused = False

    people = []
    initial_people = []

    def __init__(self):
        super().__init__()

        central_widget = QWidget()

        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.setWindowTitle("Рыбаки")
        self.setFixedSize(1366, 768)
        self.setCentralWidget(central_widget)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QPushButton {
                width: 80px;
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
                border: none;
                border-radius: 4px;
                background-color: #7c3aed;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #8b5cf6;
            }
            QPushButton:disabled {
                background-color: #a78bfa;
            }
            QLineEdit {
                padding: 6.5px;
                border: none;
                border: 1px solid #cbd5e1;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border-color: #7c3aed;
                outline: 0;
            }
            QSpinBox {
                padding: 6.5px;
                border: none;
                border: 1px solid #cbd5e1;
                border-radius: 4px;
            }
            QSpinBox:focus {
                border-color: #7c3aed;
                outline: 0;
            }
            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #cbd5e1;
                border-bottom: 1px solid #cbd5e1;
                border-top-right-radius: 4px;
            }
            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 20px;
                border-left: 1px solid #cbd5e1;
                border-bottom-right-radius: 4px;
            }
            QSpinBox::up-arrow {
                width: 10px;
                height: 10px;
                image: url(src/resources/chevron-up.svg);
            }
            QSpinBox::down-arrow {
                width: 10px;
                height: 10px;
                image: url(src/resources/chevron-down.svg);
            }
            QSlider::groove:horizontal {
                border: 1px solid #cbd5e1;
                height: 6px;
                background: #f1f5f9;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #7c3aed;
                border: 1px solid #6d28d9;
                width: 16px;
                height: 16px;
                border-radius: 8px;
                margin: -6px 0;
            }
            QSlider::handle:horizontal:hover {
                background: #6d28d9;
                border: 1px solid #5b21b6;
            }
            QSlider::handle:horizontal:pressed {
                background: #5b21b6;
            }
            QSlider::sub-page:horizontal {
                background: #7c3aed;
                border-radius: 3px;
            }
        """)

        self.load_config('src/config.json')
        self.init_menu_bar()
        self.init_area()
        self.init_controls()
        self.update_controls()

        self.game_timer = QTimer()
        self.game_timer.timeout.connect(self.game_tick)

    def load_config(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.speed = data['speed']
        self.alarm = data['alarm']
        self.people = data['people']
        self.initial_people = []

        for i, person in enumerate(data['people']):
            self.initial_people.append({
                'color': person['color'],
                'count': person['count']
            })
            self.people[i]['id'] = i

    def init_menu_bar(self):
        menu_bar = self.menuBar()

        menu_bar.setStyleSheet("""
            QMenuBar {
                background-color: #ffffff;
            }
        """)

        self.init_file_menu(menu_bar)
        self.init_settings_menu(menu_bar)
        self.init_reference_menu(menu_bar)

    def init_file_menu(self, menu_bar):
        file_menu = menu_bar.addMenu("Файл")

        self.open_file_action = QAction("Открыть", self)
        self.save_file_action = QAction("Сохранить", self)
        exit_action = QAction("Выход", self)

        self.open_file_action.triggered.connect(self.open_file)
        self.save_file_action.triggered.connect(self.save_file)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(self.open_file_action)
        file_menu.addAction(self.save_file_action)
        file_menu.addAction(exit_action)
    
    def open_file(self):
        file_path = QFileDialog.getOpenFileName(
            self,
            "Открыть файл",
            "",
            "JSON Files (*.json);;All Files (*)"
        )

        if file_path[0]:
            self.load_config(file_path[0])
            self.update_controls()
            self.update_characters_display()

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить файл",
            "",
            "JSON Files (*.json);;All Files (*)"
        )

        if file_path:
            if not file_path.endswith('.json'):
                file_path += '.json'
        
            saved_data = {
                'speed': self.speed,
                'alarm': self.alarm,
                'people': self.people,
            }

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(saved_data, f, ensure_ascii=False, indent=4)

    def update_controls(self):
        self.speed_slider.setValue(self.speed)
        self.speed_input.setText(str(self.speed))

        self.alarm_slider.setValue(self.alarm)
        self.alarm_input.setText(str(self.alarm))

    def init_settings_menu(self, menu_bar):
        settings_menu = menu_bar.addMenu("Настройки")

        self.colors_action = QAction("Выбор цвета", self)
        self.colors_action.triggered.connect(self.show_color_dialog)

        self.initial_action = QAction("Начальное заполнение", self)
        self.initial_action.triggered.connect(self.show_initial_dialog)

        settings_menu.addAction(self.colors_action)
        settings_menu.addAction(self.initial_action)

    def show_color_dialog(self):
        dialog = ColorDialog(self, people=self.people)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.people = dialog.updated_people
            self.initial_people = []

            for i, person in enumerate(self.people):
                self.initial_people.append({
                    'color': person['color'],
                    'count': person['count']
                })
                person['id'] = i

            self.update_characters_display()

    def show_initial_dialog(self):
        dialog = InitialDialog(self, people=self.people)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.people = dialog.get_updated_people()
            self.initial_people = []

            for i, person in enumerate(self.people):
                self.initial_people.append({
                    'color': person['color'],
                    'count': person['count']
                })
                person['id'] = i

            self.update_characters_display()

    def init_reference_menu(self, menu_bar):
        reference_menu = menu_bar.addMenu("Справка")

        author_action = QAction("Об авторе", self)
        author_action.triggered.connect(AuthorDialog(self).exec)

        about_menu = QAction("О программе", self)
        about_menu.triggered.connect(AboutDialog(self).exec)

        reference_menu.addAction(author_action)
        reference_menu.addAction(about_menu)

    def init_controls(self):
        controls_container = QWidget()
        controls_container.setStyleSheet("""
            QWidget {
                border-top: 1px solid #e2e8f0;
            }
            QPushButton {
                border: none;
            }
            QLineEdit:focus {
                border-top: 1px solid #7c3aed;
            }
            QSlider {
                border: none;
            }
        """)

        controls_layout = QHBoxLayout()
        controls_layout.setContentsMargins(8, 8, 8, 8)

        self.start_button = QPushButton("Старт")
        self.pause_button = QPushButton("Пауза")
        self.exit_button = QPushButton("Выход")
    
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.alarm_slider = QSlider(Qt.Orientation.Horizontal)

        self.speed_input = QLineEdit()
        self.alarm_input = QLineEdit()

        self.alarm_lamp = QLabel()
        self.alarm_lamp.setFixedSize(20, 20)
        self.alarm_lamp.setStyleSheet("""
            QLabel {
                background-color: #d1d5db;
                border-radius: 10px;
                border: 1px solid #9ca3af;
            }
        """)
        self.alarm_lamp.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.start_button.clicked.connect(self.toggle_game)
        self.pause_button.clicked.connect(self.toggle_pause)
        self.exit_button.clicked.connect(self.close)

        self.speed_slider.setMinimum(0)
        self.speed_slider.setMaximum(100)

        self.alarm_slider.setMinimum(0)
        self.alarm_slider.setMaximum(100)

        self.speed_input.setFixedWidth(40)
        self.alarm_input.setFixedWidth(40)

        self.speed_slider.valueChanged.connect(self.on_speed_changed)
        self.alarm_slider.valueChanged.connect(self.on_alarm_changed)

        self.speed_input.textChanged.connect(self.on_speed_input_changed)
        self.alarm_input.textChanged.connect(self.on_alarm_input_changed)

        # Создаем подписи и размещаем их слева от слайдеров
        speed_label = QLabel("Скорость")
        speed_label.setFixedWidth(60)
        speed_label.setStyleSheet("font-size: 12px; color: #4b5563; font-weight: bold; border: none;")
        
        alarm_label = QLabel("Аварийная лампа")
        alarm_label.setFixedWidth(110)
        alarm_label.setStyleSheet("font-size: 12px; color: #4b5563; font-weight: bold; border: none;")

        controls_layout.addWidget(self.start_button)
        controls_layout.addWidget(self.pause_button)
        controls_layout.addWidget(self.exit_button)
        
        # Добавляем скорость с подписью слева
        controls_layout.addWidget(speed_label)
        controls_layout.addWidget(self.speed_slider)
        controls_layout.addWidget(self.speed_input)
        
        # Добавляем аварийную лампу с подписью слева
        controls_layout.addWidget(alarm_label)
        controls_layout.addWidget(self.alarm_slider)
        controls_layout.addWidget(self.alarm_input)
        controls_layout.addWidget(self.alarm_lamp)

        controls_container.setLayout(controls_layout)
        self.main_layout.addWidget(controls_container)

    def on_speed_changed(self, value):
        self.speed_input.setText(str(value))
        self.speed = value

        if self.is_running and not self.is_paused:
            interval = max(10, 1000 - self.speed * 7)
            self.game_timer.setInterval(interval)

    def on_alarm_changed(self, value):
        self.alarm_input.setText(str(value))
        self.alarm = value

    def on_speed_input_changed(self, text):
        if text == "":
            # Разрешаем пустое поле
            return
            
        if text.isdigit():
            # Проверка на ведущий ноль (кроме самого "0")
            if len(text) > 1 and text.startswith('0'):
                self.speed_input.blockSignals(True)
                self.speed_input.setText(str(self.speed))
                self.speed_input.blockSignals(False)
                
                QMessageBox.warning(
                    self,
                    "Недопустимое значение",
                    "Число не должно начинаться с нуля."
                )
                return

            value = int(text)

            if value > 100:
                self.speed_input.blockSignals(True)
                self.speed_input.setText(str(self.speed))
                self.speed_input.blockSignals(False)

                QMessageBox.warning(
                    self,
                    "Недопустимое значение",
                    "Значение должно быть в диапазоне от 0 до 100."
                )
                return

            self.speed_slider.setValue(value)
            self.speed = value

            if self.is_running and not self.is_paused:
                interval = max(10, 1000 - self.speed * 7)
                self.game_timer.setInterval(interval)
        else:
            # Введены нечисловые символы - восстанавливаем предыдущее значение
            self.speed_input.blockSignals(True)
            self.speed_input.setText(str(self.speed))
            self.speed_input.blockSignals(False)

            QMessageBox.warning(
                self,
                "Ошибка ввода",
                "Разрешено вводить только числовые значения."
            )

    def on_alarm_input_changed(self, text):
        if text == "":
            # Разрешаем пустое поле
            return
            
        if text.isdigit():
            # Проверка на ведущий ноль (кроме самого "0")
            if len(text) > 1 and text.startswith('0'):
                self.alarm_input.blockSignals(True)
                self.alarm_input.setText(str(self.alarm))
                self.alarm_input.blockSignals(False)
                
                QMessageBox.warning(
                    self,
                    "Недопустимое значение",
                    "Число не должно начинаться с нуля."
                )
                return

            value = int(text)

            if value > 100:
                self.alarm_input.blockSignals(True)
                self.alarm_input.setText(str(self.alarm))
                self.alarm_input.blockSignals(False)

                QMessageBox.warning(
                    self,
                    "Недопустимое значение",
                    "Значение должно быть в диапазоне от 0 до 100."
                )
                return
            
            self.alarm_slider.setValue(value)
            self.alarm = value
        else:
            # Введены нечисловые символы - восстанавливаем предыдущее значение
            self.alarm_input.blockSignals(True)
            self.alarm_input.setText(str(self.alarm))
            self.alarm_input.blockSignals(False)

            QMessageBox.warning(
                self,
                "Ошибка ввода",
                "Разрешено вводить только числовые значения."
            )

    def init_area(self):
        self.area_container = QWidget()
        self.area_container.setStyleSheet("""
            QWidget {
                background-color: #dbeafe;
                border-top: 1px solid #e2e8f0;
            }
        """)

        self.area_layout = QHBoxLayout()
        self.area_layout.setContentsMargins(16, 16, 16, 16)
        self.area_layout.setSpacing(16)
        self.area_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.character_widgets = []
        for i in range(10):
            character_widget = QWidget()
            character_widget.setStyleSheet("""border: none""")
            character_layout = QVBoxLayout()
            character_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            character_layout.setSpacing(10)

            count_label = QLabel("0")
            count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            count_label.setStyleSheet("""
                font-size: 18px; 
                font-weight: bold;
                padding: 5px;
                color: black;
            """)

            fisher_widget = Fisher()
            fisher_widget.setFixedSize(112, 220)

            character_layout.addWidget(count_label)
            character_layout.addWidget(fisher_widget)
            character_widget.setLayout(character_layout)

            self.character_widgets.append({
                'widget': character_widget,
                'fisher_widget': fisher_widget,
                'count_label': count_label,
                'highlight_timer': None,
                'animation': None
            })

            self.area_layout.addWidget(character_widget)

        self.area_container.setLayout(self.area_layout)
        self.main_layout.addWidget(self.area_container, 1)

        self.update_characters_display()

    def update_characters_display(self):
        for i, character_data in enumerate(self.character_widgets):
            if i < len(self.people):
                person = self.people[i]

                character_data['fisher_widget'].update_color(person['color'])
                character_data['count_label'].setText(str(person['count']))
                
                if person['count'] >= 10:
                    character_data['count_label'].setStyleSheet("""
                        font-size: 18px; 
                        font-weight: bold; 
                        padding: 5px;
                        color: #16a34a;
                    """)
                else:
                    character_data['count_label'].setStyleSheet("""
                        font-size: 18px; 
                        font-weight: bold; 
                        padding: 5px;
                        color: black;
                    """)
            else:
                character_data['fisher_widget'].update_color("#ffffff")
                character_data['count_label'].setText("0")
                character_data['count_label'].setStyleSheet("""
                    font-size: 18px; 
                    font-weight: bold; 
                    padding: 5px;
                    color: black;
                """)

    def update_character_display(self, index):
        if index < len(self.people):
            person = self.people[index]
            character_data = self.character_widgets[index]
            character_data['count_label'].setText(str(person['count']))
            
            if person['count'] >= 10:
                character_data['count_label'].setStyleSheet("""
                    font-size: 18px; 
                    font-weight: bold; 
                    padding: 5px;
                    color: #16a34a;
                """)
            else:
                character_data['count_label'].setStyleSheet("""
                    font-size: 18px; 
                    font-weight: bold; 
                    padding: 5px;
                    color: black;
                """)

    def highlight_character(self, index):
        """Обычная подсветка персонажа (без изменения цвета счетчика)"""
        if index < len(self.character_widgets):
            character_data = self.character_widgets[index]
            
            # Анимация движения Fisher вниз и обратно
            self.animate_fisher_movement(index)
            
            if character_data['highlight_timer']:
                character_data['highlight_timer'].stop()
            
            character_data['highlight_timer'] = QTimer()
            character_data['highlight_timer'].setSingleShot(True)
            character_data['highlight_timer'].timeout.connect(
                lambda: self.restore_character_style(index)
            )
            character_data['highlight_timer'].start(200)

    def highlight_character_with_red_counter(self, index):
        """Подсветка персонажа с красным цветом счетчика при аварии"""
        if index < len(self.character_widgets):
            character_data = self.character_widgets[index]
            
            # Устанавливаем красный цвет счетчика
            character_data['count_label'].setStyleSheet("""
                font-size: 18px; 
                font-weight: bold; 
                padding: 5px;
                color: #ef4444;
            """)
            
            # Анимация движения Fisher вниз и обратно
            self.animate_fisher_movement(index)
            
            if character_data['highlight_timer']:
                character_data['highlight_timer'].stop()
            
            character_data['highlight_timer'] = QTimer()
            character_data['highlight_timer'].setSingleShot(True)
            character_data['highlight_timer'].timeout.connect(
                lambda: self.restore_character_style_after_alarm(index)
            )
            character_data['highlight_timer'].start(500)  # Увеличиваем время до 500 мс

    def animate_fisher_movement(self, index):
        """Анимация движения Fisher вниз и обратно"""
        if index < len(self.character_widgets):
            character_data = self.character_widgets[index]
            fisher_widget = character_data['fisher_widget']
            
            animation = QPropertyAnimation(fisher_widget, b"geometry")
            animation.setDuration(300)
            animation.setEasingCurve(QEasingCurve.Type.OutInQuad)
            
            current_geometry = fisher_widget.geometry()
            
            down_geometry = current_geometry.translated(0, 20)
            up_geometry = current_geometry
            
            animation.setKeyValueAt(0, current_geometry)
            animation.setKeyValueAt(0.5, down_geometry)
            animation.setKeyValueAt(1, up_geometry)

            animation.start()
            character_data['animation'] = animation

    def restore_character_style(self, index):
        """Восстанавливаем стиль Fisher (убираем обводку)"""
        if index < len(self.character_widgets):
            character_data = self.character_widgets[index]
            # Убираем обводку
            character_data['fisher_widget'].setStyleSheet("")

    def restore_character_style_after_alarm(self, index):
        """Восстанавливаем нормальный цвет счетчика после аварии"""
        if index < len(self.character_widgets):
            character_data = self.character_widgets[index]
            
            # Восстанавливаем нормальный цвет счетчика
            person = self.people[index]
            if person['count'] >= 10:
                character_data['count_label'].setStyleSheet("""
                    font-size: 18px; 
                    font-weight: bold; 
                    padding: 5px;
                    color: #16a34a;
                """)
            else:
                character_data['count_label'].setStyleSheet("""
                    font-size: 18px; 
                    font-weight: bold; 
                    padding: 5px;
                    color: black;
                """)
            
            # Убираем обводку с Fisher
            character_data['fisher_widget'].setStyleSheet("")

    def trigger_alarm_lamp(self):
        self.alarm_lamp.setStyleSheet("""
            QLabel {
                background-color: #ef4444;
                border-radius: 10px;
                border: 1px solid #dc2626;
            }
        """)
        
        QTimer.singleShot(500, self.reset_alarm_lamp)

    def reset_alarm_lamp(self):
        self.alarm_lamp.setStyleSheet("""
            QLabel {
                background-color: #d1d5db;
                border-radius: 10px;
                border: 1px solid #9ca3af;
            }
        """)

    def game_tick(self):
        # Проверяем, должна ли произойти авария (с процентной вероятностью)
        if self.alarm > 0 and random.randint(1, 100) <= self.alarm:
            self.trigger_alarm()
        else:
            # Обычный ход игры - увеличение счетчика
            self.normal_game_tick()

    def normal_game_tick(self):
        """Обычный ход игры - увеличение счетчика"""
        available_people = [p for p in self.people if p['count'] < 10]

        if not available_people:
            self.stop_game_with_message()
            return

        selected_person = random.choice(available_people)
        person_index = self.people.index(selected_person)
        selected_person['count'] += 1

        self.update_character_display(person_index)
        self.highlight_character(person_index)

    def trigger_alarm(self):
        """Обработка аварии - уменьшение счетчика и включение лампы"""
        # Включаем красную лампу
        self.trigger_alarm_lamp()
        
        # Находим подходящих персонажей для уменьшения счетчика
        eligible_people = [p for p in self.people if 1 <= p['count'] <= 9]

        if not eligible_people:
            return
        
        # Уменьшаем счетчик случайному персонажу
        selected_person = random.choice(eligible_people)
        person_index = self.people.index(selected_person)
        selected_person['count'] -= 1
        
        self.update_character_display(person_index)
        self.highlight_character_with_red_counter(person_index)

    def toggle_game(self):
        if not self.is_running:
            self.start_game()
        else:
            self.stop_game()

    def start_game(self):
        self.is_running = True
        self.is_paused = False
        self.start_button.setText("Стоп")
        self.set_menu_enabled(False)

        interval = max(10, 1000 - self.speed * 7)
        self.game_timer.start(interval)

    def stop_game(self):
        self.is_running = False
        self.is_paused = False
        self.start_button.setText("Старт")

        self.reset_game()        
        self.set_menu_enabled(True)
        self.update_characters_display()

        self.game_timer.stop()

    def stop_game_with_message(self):
        """Остановка игры с сообщением о завершении (без сброса)"""
        self.is_running = False
        self.is_paused = False
        self.start_button.setText("Старт")
        
        self.set_menu_enabled(True)
        self.game_timer.stop()
        
        # Показываем сообщение о завершении игры
        QMessageBox.information(
            self,
            "Игра завершена",
            "Игра заверешена\n"
            "Нажмите 'Старт' для начала новой игры."
        )

    def set_menu_enabled(self, enabled):
        self.open_file_action.setEnabled(enabled)
        self.save_file_action.setEnabled(enabled)
        self.colors_action.setEnabled(enabled)
        self.initial_action.setEnabled(enabled)

    def reset_game(self):
        """Сброс игры к начальным значениям"""
        self.people = []

        for i, person in enumerate(self.initial_people):
            self.people.append({
                'id': i,
                'color': person['color'],
                'count': person['count']
            })

    def toggle_pause(self):
        if not self.is_paused:
            self.pause_game()
        else:
            self.resume_game()

    def pause_game(self):
        self.is_paused = True
        self.pause_button.setText("Продолжить")
        self.game_timer.stop()

    def resume_game(self):
        self.is_paused = False
        self.pause_button.setText("Пауза")
        interval = max(10, 1000 - self.speed * 7)
        self.game_timer.start(interval)