from PyQt6.QtWidgets import (
    QVBoxLayout, QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QFrame
)
from PyQt6.QtCore import Qt

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("О программе")
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

        title_label = QLabel("О программе")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            margin: 10px 0px;
        """)

        desc_frame = QFrame()
        desc_frame.setStyleSheet("""
            QFrame {
                background: #f8f9fa;
                border-radius: 8px;
            }
        """)
        desc_layout = QVBoxLayout(desc_frame)
        desc_layout.setContentsMargins(15, 15, 15, 15)

        info_label = QLabel(
            "Рыбаки\n"
            "• Есть 10 рыбаков\n"
            "• У каждого в начале от 0 до 9 рыб\n"
            "• Случайным образом выбирается рыбак и ему добавляется 1 рыба\n"
            "• При срабатывании аварийной лампы случайно выбирается рыбак,\n  у которого от 1 до 9 рыб\n"
            "• Игра заканчивается, когда все поймали по 10 рыб"
        )
        info_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        info_label.setStyleSheet("""
            font-size: 12px;
            line-height: 1.4;
            margin: 5px;
        """)
        info_label.setWordWrap(True)

        desc_layout.addWidget(info_label)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)

        layout.addWidget(title_label)
        layout.addWidget(desc_frame)
        layout.addStretch()
        layout.addWidget(button_box, 0, Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)
