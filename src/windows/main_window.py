import json
import random

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QDialog, QFileDialog,
    QLineEdit, QSlider, QPushButton, QMessageBox, QLabel
)
from PyQt6.QtGui import QAction, QIntValidator, QPixmap
from dialogs.author_dialog import AuthorDialog
from dialogs.about_dialog import AboutDialog
from dialogs.color_dialog import ColorDialog
from dialogs.initial_dialog import InitialDialog

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

    def load_config(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.speed = data['speed']
        self.alarm = data['alarm']
        self.people = data['people']
        self.initial_people = data['people']

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
            self.initial_people = self.people

    def show_initial_dialog(self):
        dialog = InitialDialog(self, people=self.people)
        dialog.exec()

        # if dialog.exec() == QDialog.DialogCode.Accepted:
        #     self.people = dialog.updated_people
        #     self.initial_people = self.people

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

        self.speed_slider.setMinimum(0)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setTickPosition(QSlider.TickPosition.TicksBelow)

        self.alarm_slider.setMinimum(0)
        self.alarm_slider.setMaximum(100)
        self.alarm_slider.setTickPosition(QSlider.TickPosition.TicksBelow)

        self.speed_input.setFixedWidth(40)
        self.alarm_input.setFixedWidth(40)

        self.speed_slider.valueChanged.connect(self.on_speed_changed)
        self.alarm_slider.valueChanged.connect(self.on_alarm_changed)

        self.speed_input.textChanged.connect(self.on_speed_input_changed)
        self.alarm_input.textChanged.connect(self.on_alarm_input_changed)

        self.exit_button.clicked.connect(self.close)

        controls_layout.addWidget(self.start_button)
        controls_layout.addWidget(self.pause_button)
        controls_layout.addWidget(self.exit_button)
        controls_layout.addWidget(self.speed_slider)
        controls_layout.addWidget(self.speed_input)
        controls_layout.addWidget(self.alarm_slider)
        controls_layout.addWidget(self.alarm_input)

        controls_container.setLayout(controls_layout)
        self.main_layout.addWidget(controls_container)

    def on_speed_changed(self, value):
        self.speed_input.setText(str(value))
        self.speed = value

    def on_alarm_changed(self, value):
        self.alarm_input.setText(str(value))
        self.alarm = value

    def on_speed_input_changed(self, text):
        if text:
            if text.isdigit():
                value = int(text)

                if len(text) > 1 and text.startswith('0'):
                    if text.count('0') == len(text):
                        self.speed_input.blockSignals(True)
                        self.speed_input.setText("0")
                        self.speed_input.blockSignals(False)

                        value = 0
                    else:
                        normalized_text = text.lstrip('0')

                        if not normalized_text:
                            normalized_text = "0"
                            value = 0
                        else:
                            value = int(normalized_text)

                        self.speed_input.blockSignals(True)
                        self.speed_input.setText(normalized_text)
                        self.speed_input.blockSignals(False)

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
            else:
                self.speed_input.blockSignals(True)
                self.speed_input.setText(str(self.speed))
                self.speed_input.blockSignals(False)

                QMessageBox.warning(
                    self,
                    "Недопустимое значение",
                    "Разрешено вводить только числовое значение."
                )

    def on_alarm_input_changed(self, text):
        if text:
            if text.isdigit():
                value = int(text)

                if len(text) > 1 and text.startswith('0'):
                    if text.count('0') == len(text):
                        self.alarm_input.blockSignals(True)
                        self.alarm_input.setText("0")
                        self.alarm_input.blockSignals(False)

                        value = 0
                    else:
                        normalized_text = text.lstrip('0')

                        if not normalized_text:
                            normalized_text = "0"
                            value = 0
                        else:
                            value = int(normalized_text)

                        self.alarm_input.blockSignals(True)
                        self.alarm_input.setText(normalized_text)
                        self.alarm_input.blockSignals(False)

                if value > 100:
                    self.alarm_input.blockSignals(True)
                    self.alarm_input.setText(str(self.speed))
                    self.alarm_input.blockSignals(False)

                    QMessageBox.warning(
                        self,
                        "Недопустимое значение",
                        "Значение должно быть в диапазоне от 0 до 100."
                    )

                    return
            else:
                self.alarm_input.blockSignals(True)
                self.alarm_input.setText(str(self.alarm))
                self.alarm_input.blockSignals(False)

                QMessageBox.warning(
                    self,
                    "Недопустимое значение",
                    "Разрешено вводить только числовое значение."
                )

    def init_area(self):
        self.area_container = QWidget()
        self.area_container.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-top: 1px solid #e2e8f0;
            }
        """)

        self.area_layout = QHBoxLayout()
        self.area_layout.setContentsMargins(0, 0, 0, 0)
        self.area_layout.setSpacing(0)

        self.area_container.setLayout(self.area_layout)
        self.main_layout.addWidget(self.area_container, 1)
