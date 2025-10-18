from PyQt6.QtWidgets import (
    QVBoxLayout, QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QFrame
)
from PyQt6.QtCore import Qt

class AuthorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Об авторе")
        self.setFixedSize(640, 360)

        self.setStyleSheet("""
            QDialog {
                background: white;
            }
            QLabel {
                background: transparent;
            }
            QDialogButtonBox {
                background: transparent;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title_label = QLabel("Об авторе")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            margin: 10px 0px;
        """)

        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background: #f8f9fa;
                border-radius: 8px;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(15, 15, 15, 15)

        name_label = QLabel("Выполнил: Макаров Станислав Алексеевич")
        name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        name_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 5px;")

        group_label = QLabel("Группа: ИВТб-2301-05-00")
        group_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        group_label.setStyleSheet("font-size: 12px; margin: 5px;")

        info_layout.addWidget(name_label)
        info_layout.addWidget(group_label)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)

        layout.addWidget(title_label)
        layout.addWidget(info_frame)
        layout.addStretch()
        layout.addWidget(button_box, 0, Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)
