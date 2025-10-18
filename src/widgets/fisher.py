from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtSvgWidgets import QSvgWidget

class Fisher(QWidget):
    def __init__(self, color="black"):
        super().__init__()
        self.color = color
        self.initUI()

    def initUI(self):
        combined_svg = f'''
        <svg width="115" height="235" viewBox="0 0 115 235" fill="none" xmlns="http://www.w3.org/2000/svg">
            <line x1="52.4515" y1="1.62176" x2="112.969" y2="233.867" stroke="#713F12" stroke-width="3"/>
            <path d="M52.7581 3.19009L21 67.0338" stroke="{self.color}"/>
            <path d="M56 127C63.8399 127 71.7177 129.157 80.2363 133.528C92.1943 139.664 97.5522 146.563 104.521 158.483C108.139 164.67 109.977 172.44 110.668 180.681C111.358 188.912 110.899 197.548 109.974 205.419C109.049 213.286 107.66 220.366 106.503 225.48C105.924 228.037 105.404 230.1 105.028 231.522C104.865 232.14 104.729 232.636 104.628 233H7.37207C7.27104 232.636 7.13461 232.14 6.97168 231.522C6.59642 230.1 6.07557 228.037 5.49707 225.48C4.33974 220.366 2.95141 213.286 2.02637 205.419C1.10093 197.548 0.641794 188.912 1.33203 180.681C2.02304 172.44 3.8613 164.67 7.47852 158.483C14.4478 146.563 19.8057 139.664 31.7637 133.528C40.2823 129.157 48.1601 127 56 127Z" fill="{self.color}" stroke="{self.color}" stroke-width="2"/>
            <circle cx="56" cy="92" r="30" fill="#FED7AA"/>
        </svg>
        '''

        self.svg_widget = QSvgWidget()
        self.svg_widget.renderer().load(combined_svg.encode('utf-8'))

        layout = QVBoxLayout()
        layout.addWidget(self.svg_widget)
        self.setLayout(layout)

        self.setMinimumSize(115, 235)

    def update_color(self, new_color):
        """Метод для обновления цвета фигуры"""
        self.color = new_color
        combined_svg = f'''
        <svg width="115" height="235" viewBox="0 0 115 235" fill="none" xmlns="http://www.w3.org/2000/svg">
            <line x1="52.4515" y1="1.62176" x2="112.969" y2="233.867" stroke="#713F12" stroke-width="3"/>
            <path d="M52.7581 3.19009L21 67.0338" stroke="{self.color}"/>
            <path d="M56 127C63.8399 127 71.7177 129.157 80.2363 133.528C92.1943 139.664 97.5522 146.563 104.521 158.483C108.139 164.67 109.977 172.44 110.668 180.681C111.358 188.912 110.899 197.548 109.974 205.419C109.049 213.286 107.66 220.366 106.503 225.48C105.924 228.037 105.404 230.1 105.028 231.522C104.865 232.14 104.729 232.636 104.628 233H7.37207C7.27104 232.636 7.13461 232.14 6.97168 231.522C6.59642 230.1 6.07557 228.037 5.49707 225.48C4.33974 220.366 2.95141 213.286 2.02637 205.419C1.10093 197.548 0.641794 188.912 1.33203 180.681C2.02304 172.44 3.8613 164.67 7.47852 158.483C14.4478 146.563 19.8057 139.664 31.7637 133.528C40.2823 129.157 48.1601 127 56 127Z" fill="{self.color}" stroke="{self.color}" stroke-width="2"/>
            <circle cx="56" cy="92" r="30" fill="#FED7AA"/>
        </svg>
        '''
        self.svg_widget.renderer().load(combined_svg.encode('utf-8'))
