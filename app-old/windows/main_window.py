import json
import random
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QSlider, QDialog, QFileDialog, QMessageBox, QLabel
)
from PyQt6.QtGui import QAction, QIntValidator, QPixmap
from widgets.about_dialog import AboutDialog
from widgets.author_dialog import AuthorDialog
from widgets.color_dialog import ColorDialog
from widgets.initial_dialog import InitialDialog

class MainWindow(QMainWindow):
    speed = 0
    alarm = 0
    people = []
    initial_people_state = []  # Сохраняем начальное состояние персонажей
    game_timer = None
    is_game_running = False
    is_game_paused = False

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
                background-color: #000000;
            }
        """)

        self.load_default_config()
        self.init_menu_bar()
        self.init_area()
        self.init_controls()
        self.update_controls_from_data()
        
        # Таймер для игры
        self.game_timer = QTimer()
        self.game_timer.timeout.connect(self.game_tick)

    def load_default_config(self):
        try:
            with open('app/config.default.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.speed = data.get('speed', 0)
            self.alarm = data.get('alarm', 0)
            self.people = data.get('people', [])
            # Сохраняем начальное состояние
            self.initial_people_state = [person.copy() for person in self.people]
        except Exception as e:
            print(f"Ошибка загрузки конфигурации по умолчанию: {e}")
            self.speed = 0
            self.alarm = 0
            self.people = []
            self.initial_people_state = []

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

        # Подключаем действия к методам
        self.open_file_action.triggered.connect(self.open_file)
        self.save_file_action.triggered.connect(self.save_file)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(self.open_file_action)
        file_menu.addAction(self.save_file_action)
        file_menu.addAction(exit_action)

    def open_file(self):
        """Открывает JSON-файл и загружает данные"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Открыть файл",
                "",
                "JSON Files (*.json);;All Files (*)"
            )
            
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Обновляем данные из файла
                self.speed = data.get('speed', self.speed)
                self.alarm = data.get('alarm', self.alarm)
                self.people = data.get('people', self.people)
                # Сохраняем начальное состояние
                self.initial_people_state = [person.copy() for person in self.people]
                
                # Обновляем элементы управления
                self.update_controls_from_data()
                self.update_characters_display()
                
                QMessageBox.information(
                    self,
                    "Успех",
                    f"Файл успешно загружен:\n{file_path}"
                )
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось открыть файл:\n{str(e)}"
            )

    def save_file(self):
        """Сохраняет данные в JSON-файл"""
        try:
            # Обновляем данные из элементов управления
            self.update_data_from_controls()
            
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Сохранить файл",
                "",
                "JSON Files (*.json);;All Files (*)"
            )
            
            if file_path:
                if not file_path.endswith('.json'):
                    file_path += '.json'
                
                data_to_save = {
                    'speed': self.speed,
                    'alarm': self.alarm,
                    'people': self.people
                }
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data_to_save, f, ensure_ascii=False, indent=4)
                
                QMessageBox.information(
                    self,
                    "Успех",
                    f"Файл успешно сохранен:\n{file_path}"
                )
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось сохранить файл:\n{str(e)}"
            )

    def update_controls_from_data(self):
        """Обновляет элементы управления из данных"""
        try:
            # Обновляем слайдер скорости
            self.speed_slider.setValue(self.speed)
            self.speed_input.setText(str(self.speed))
            
            # Обновляем слайдер тревоги
            self.alarm_slider.setValue(self.alarm)
            self.alarm_input.setText(str(self.alarm))
            
        except Exception as e:
            print(f"Ошибка обновления элементов управления: {e}")

    def update_data_from_controls(self):
        """Обновляет данные из элементов управления"""
        try:
            # Обновляем скорость из слайдера
            self.speed = self.speed_slider.value()
            
            # Обновляем тревогу из слайдера
            self.alarm = self.alarm_slider.value()
            
        except Exception as e:
            print(f"Ошибка обновления данных из элементов управления: {e}")

    def init_settings_menu(self, menu_bar):
        settings_menu = menu_bar.addMenu("Настройки")

        self.colors_action = QAction("Выбор цвета", self)
        self.colors_action.triggered.connect(self.show_color_dialog)

        self.initial_action = QAction("Начальное заполнение", self)
        self.initial_action.triggered.connect(self.show_initial_dialog)

        settings_menu.addAction(self.colors_action)
        settings_menu.addAction(self.initial_action)

    def show_color_dialog(self):
        """Показывает диалог выбора цвета и сохраняет изменения при нажатии OK"""
        dialog = ColorDialog(self, people=self.people)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.people = dialog.get_updated_people
            # Обновляем начальное состояние
            self.initial_people_state = [person.copy() for person in self.people]
            self.update_characters_display()
    
    def show_initial_dialog(self):
        """Показывает диалог начального заполнения и обновляет данные при принятии"""
        dialog = InitialDialog(self.people, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.people = dialog.get_updated_people
            # Обновляем начальное состояние
            self.initial_people_state = [person.copy() for person in self.people]
            self.update_characters_display()

    def init_reference_menu(self, menu_bar):
        reference_menu = menu_bar.addMenu("Справка")

        author_action = QAction("Об авторе", self)
        author_action.triggered.connect(AuthorDialog(self).exec)

        about_menu = QAction("О программе", self)
        about_menu.triggered.connect(AboutDialog(self).exec)

        reference_menu.addAction(author_action)
        reference_menu.addAction(about_menu)

    def init_area(self):
        self.area_container = QWidget()
        self.area_container.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-top: 1px solid #e2e8f0;
            }
        """)

        self.area_layout = QHBoxLayout()
        self.area_layout.setSpacing(10)
        self.area_layout.setContentsMargins(20, 20, 20, 20)

        # Создаем виджеты для 10 персонажей
        self.character_widgets = []
        for i in range(10):
            character_widget = QWidget()
            character_layout = QVBoxLayout()
            
            # Метка для отображения спрайта
            sprite_label = QLabel()
            sprite_label.setFixedSize(80, 80)
            sprite_label.setStyleSheet("border: 1px solid #ccc;")
            sprite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Метка для отображения счета
            count_label = QLabel("0")
            count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            count_label.setStyleSheet("font-size: 16px; font-weight: bold;")
            
            character_layout.addWidget(sprite_label)
            character_layout.addWidget(count_label)
            character_widget.setLayout(character_layout)
            
            self.character_widgets.append({
                'widget': character_widget,
                'sprite_label': sprite_label,
                'count_label': count_label
            })
            
            self.area_layout.addWidget(character_widget)

        self.area_container.setLayout(self.area_layout)
        self.main_layout.addWidget(self.area_container, 1)
        
        # Обновляем отображение персонажей
        self.update_characters_display()

    def update_characters_display(self):
        """Обновляет отображение персонажей в соответствии с данными people"""
        for i, character_data in enumerate(self.character_widgets):
            if i < len(self.people):
                person = self.people[i]
                
                # Устанавливаем цвет фона
                color_style = f"background-color: {person['color']}; border: 1px solid #ccc;"
                character_data['sprite_label'].setStyleSheet(color_style)
                
                # Устанавливаем счет
                character_data['count_label'].setText(str(person['count']))
                
                # Сбрасываем стиль счетчика
                character_data['count_label'].setStyleSheet("font-size: 16px; font-weight: bold;")
            else:
                # Если данных нет, устанавливаем значения по умолчанию
                character_data['sprite_label'].setStyleSheet("background-color: #ffffff; border: 1px solid #ccc;")
                character_data['count_label'].setText("0")

    def init_controls(self):
        controls_container = QWidget()
        controls_container.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-top: 1px solid #e2e8f0;
            }
        """)

        controls_layout = QHBoxLayout()

        self.start_button = QPushButton("Старт")
        self.pause_button = QPushButton("Пауза")
        self.exit_button = QPushButton("Выход")
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_input = QLineEdit()
        self.alarm_slider = QSlider(Qt.Orientation.Horizontal)
        self.alarm_input = QLineEdit()

        # Настройка слайдера скорости
        self.speed_slider.setMinimum(0)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        
        # Настройка слайдера тревоги
        self.alarm_slider.setMinimum(0)
        self.alarm_slider.setMaximum(100)
        self.alarm_slider.setTickPosition(QSlider.TickPosition.TicksBelow)

        # Добавляем валидаторы для полей ввода
        int_validator = QIntValidator(0, 100, self)
        self.speed_input.setValidator(int_validator)
        self.alarm_input.setValidator(int_validator)

        # Связываем слайдеры с полями ввода
        self.speed_slider.valueChanged.connect(self.on_speed_changed)
        self.alarm_slider.valueChanged.connect(self.on_alarm_changed)
        
        self.speed_input.textChanged.connect(self.on_speed_input_changed)
        self.alarm_input.textChanged.connect(self.on_alarm_input_changed)

        # Кнопка выхода
        self.exit_button.clicked.connect(self.close)
        
        # Кнопки управления игрой
        self.start_button.clicked.connect(self.toggle_game)
        self.pause_button.clicked.connect(self.toggle_pause)
        
        # Изначально кнопка паузы неактивна
        self.pause_button.setEnabled(False)

        controls_layout.addWidget(self.start_button)
        controls_layout.addWidget(self.pause_button)
        controls_layout.addWidget(self.exit_button)
        controls_layout.addWidget(self.speed_slider)
        controls_layout.addWidget(self.speed_input)
        controls_layout.addWidget(self.alarm_slider)
        controls_layout.addWidget(self.alarm_input)

        controls_container.setLayout(controls_layout)
        self.main_layout.addWidget(controls_container)

    def toggle_game(self):
        """Переключает состояние игры (старт/стоп)"""
        if not self.is_game_running:
            self.start_game()
        else:
            self.stop_game()

    def is_game_finished(self):
        """Проверяет, закончена ли игра (все персонажи набрали по 10 очков)"""
        if not self.people:
            return False
        return all(person['count'] >= 10 for person in self.people)

    def reset_game(self):
        """Сбрасывает игру к начальному состоянию"""
        # Восстанавливаем начальное состояние персонажей
        if self.initial_people_state:
            self.people = [person.copy() for person in self.initial_people_state]
        else:
            # Если начальное состояние не сохранено, сбрасываем счетчики на 0
            for person in self.people:
                person['count'] = 0
        
        # Обновляем отображение
        self.update_characters_display()

    def start_game(self):
        """Запускает игру"""
        self.is_game_running = True
        self.is_game_paused = False
        self.start_button.setText("Стоп")
        self.pause_button.setEnabled(True)
        self.pause_button.setText("Пауза")
        
        # Блокируем меню
        self.set_menu_enabled(False)
        
        # Запускаем таймер игры
        interval = max(10, 1000 - self.speed * 10)  # Скорость влияет на интервал
        self.game_timer.start(interval)

    def stop_game(self):
        """Останавливает игру и сбрасывает очки"""
        self.is_game_running = False
        self.is_game_paused = False
        self.start_button.setText("Старт")
        self.pause_button.setText("Пауза")
        self.pause_button.setEnabled(False)
        
        # Сбрасываем игру к начальному состоянию
        self.reset_game()
        
        # Разблокируем меню
        self.set_menu_enabled(True)
        
        # Останавливаем таймер
        self.game_timer.stop()

    def set_menu_enabled(self, enabled):
        """Блокирует или разблокирует пункты меню"""
        self.open_file_action.setEnabled(enabled)
        self.save_file_action.setEnabled(enabled)
        self.colors_action.setEnabled(enabled)
        self.initial_action.setEnabled(enabled)

    def toggle_pause(self):
        """Переключает состояние паузы"""
        if self.is_game_running:
            if not self.is_game_paused:
                self.pause_game()
            else:
                self.resume_game()

    def pause_game(self):
        """Ставит игру на паузу"""
        self.is_game_paused = True
        self.pause_button.setText("Продолжить")
        self.game_timer.stop()

    def resume_game(self):
        """Продолжает игру после паузы"""
        self.is_game_paused = False
        self.pause_button.setText("Пауза")
        interval = max(10, 1000 - self.speed * 10)
        self.game_timer.start(interval)

    def game_tick(self):
        """Один тик игры - случайный персонаж получает очко"""
        # Проверяем, есть ли персонажи, которые еще не набрали 10 очков
        available_people = [p for p in self.people if p['count'] < 10]
        
        if not available_people:
            # Все набрали по 10 очков - игра окончена
            self.stop_game()
            QMessageBox.information(self, "Игра окончена", "Все персонажи набрали по 10 очков!")
            return
        
        # Выбираем случайного персонажа
        selected_person = random.choice(available_people)
        person_index = self.people.index(selected_person)
        
        # Увеличиваем счет
        selected_person['count'] += 1
        
        # Обновляем отображение
        self.update_character_display(person_index)
        
        # Визуальный эффект - подсвечиваем персонажа
        self.highlight_character(person_index)
        
        # Проверяем, не набрал ли персонаж 10 очков
        if selected_person['count'] >= 10:
            self.character_widgets[person_index]['count_label'].setStyleSheet(
                "font-size: 16px; font-weight: bold; color: red;"
            )

    def update_character_display(self, index):
        """Обновляет отображение конкретного персонажа"""
        if index < len(self.people):
            person = self.people[index]
            self.character_widgets[index]['count_label'].setText(str(person['count']))

    def highlight_character(self, index):
        """Подсвечивает персонажа при получении очка"""
        original_style = self.character_widgets[index]['sprite_label'].styleSheet()
        
        # Меняем цвет на более светлый
        highlighted_style = original_style.replace(
            f"background-color: {self.people[index]['color']};", 
            f"background-color: {self.lighten_color(self.people[index]['color'])};"
        )
        self.character_widgets[index]['sprite_label'].setStyleSheet(highlighted_style)
        
        # Возвращаем оригинальный цвет через 150 мс (без приостановки игры)
        QTimer.singleShot(150, lambda: self.restore_character_style(index, original_style))

    def restore_character_style(self, index, original_style):
        """Восстанавливает оригинальный стиль персонажа"""
        self.character_widgets[index]['sprite_label'].setStyleSheet(original_style)

    def lighten_color(self, hex_color, factor=0.3):
        """Осветляет hex-цвет на заданный фактор"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        
        return f"#{r:02x}{g:02x}{b:02x}"

    def on_speed_changed(self, value):
        """Обработчик изменения слайдера скорости"""
        self.speed_input.setText(str(value))
        self.speed = value
        
        # Обновляем интервал таймера, если игра запущена
        if self.is_game_running and not self.is_game_paused:
            interval = max(10, 1000 - self.speed * 10)
            self.game_timer.setInterval(interval)

    def on_alarm_changed(self, value):
        """Обработчик изменения слайдера тревоги"""
        self.alarm_input.setText(str(value))
        self.alarm = value

    def on_speed_input_changed(self, text):
        """Обработчик изменения поля ввода скорости"""
        if text:
            # Проверяем, является ли текст числом
            if text.isdigit():
                value = int(text)
                
                # Убираем ведущие нули из чисел
                if len(text) > 1 and text.startswith('0'):
                    # Если все символы - нули, оставляем один ноль
                    if text.count('0') == len(text):
                        self.speed_input.blockSignals(True)
                        self.speed_input.setText("0")
                        self.speed_input.blockSignals(False)
                        value = 0
                    else:
                        # Убираем ведущие нули перед числами (например, 00050 -> 50)
                        normalized_text = text.lstrip('0')
                        # Если после удаления нулей строка пуста, устанавливаем 0
                        if not normalized_text:
                            normalized_text = "0"
                            value = 0
                        else:
                            value = int(normalized_text)
                        
                        self.speed_input.blockSignals(True)
                        self.speed_input.setText(normalized_text)
                        self.speed_input.blockSignals(False)
                
                # Проверяем, что значение не превышает 100
                if value > 100:
                    # Восстанавливаем предыдущее значение
                    self.speed_input.blockSignals(True)
                    self.speed_input.setText(str(self.speed))
                    self.speed_input.blockSignals(False)
                    
                    # Показываем сообщение об ошибке
                    QMessageBox.warning(
                        self,
                        "Недопустимое значение",
                        "Значение скорости должно быть в диапазоне от 0 до 100."
                    )
                    return
                
                # Обновляем слайдер и значение
                self.speed_slider.setValue(value)
                self.speed = value
                
                # Обновляем интервал таймера, если игра запущена
                if self.is_game_running and not self.is_game_paused:
                    interval = max(10, 1000 - self.speed * 10)
                    self.game_timer.setInterval(interval)
            else:
                # Если введены не цифры, восстанавливаем предыдущее значение
                self.speed_input.blockSignals(True)
                self.speed_input.setText(str(self.speed))
                self.speed_input.blockSignals(False)
                
                # Показываем сообщение об ошибке
                QMessageBox.warning(
                    self,
                    "Недопустимый ввод",
                    "Разрешены только цифровые значения."
                )

    def on_alarm_input_changed(self, text):
        """Обработчик изменения поля ввода тревоги"""
        if text:
            # Проверяем, является ли текст числом
            if text.isdigit():
                value = int(text)
                
                # Убираем ведущие нули из чисел
                if len(text) > 1 and text.startswith('0'):
                    # Если все символы - нули, оставляем один ноль
                    if text.count('0') == len(text):
                        self.alarm_input.blockSignals(True)
                        self.alarm_input.setText("0")
                        self.alarm_input.blockSignals(False)
                        value = 0
                    else:
                        # Убираем ведущие нули перед числами (например, 00050 -> 50)
                        normalized_text = text.lstrip('0')
                        # Если после удаления нулей строка пуста, устанавливаем 0
                        if not normalized_text:
                            normalized_text = "0"
                            value = 0
                        else:
                            value = int(normalized_text)
                        
                        self.alarm_input.blockSignals(True)
                        self.alarm_input.setText(normalized_text)
                        self.alarm_input.blockSignals(False)
                
                # Проверяем, что значение не превышает 100
                if value > 100:
                    # Восстанавливаем предыдущее значение
                    self.alarm_input.blockSignals(True)
                    self.alarm_input.setText(str(self.alarm))
                    self.alarm_input.blockSignals(False)
                    
                    # Показываем сообщение об ошибке
                    QMessageBox.warning(
                        self,
                        "Недопустимое значение",
                        "Значение тревоги должно быть в диапазоне от 0 до 100."
                    )
                    return
                
                # Обновляем слайдер и значение
                self.alarm_slider.setValue(value)
                self.alarm = value
            else:
                # Если введены не цифры, восстанавливаем предыдущее значение
                self.alarm_input.blockSignals(True)
                self.alarm_input.setText(str(self.alarm))
                self.alarm_input.blockSignals(False)
                
                # Показываем сообщение об ошибке
                QMessageBox.warning(
                    self,
                    "Недопустимый ввод",
                    "Разрешены только цифровые значения."
                )