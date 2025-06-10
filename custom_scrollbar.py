from PyQt5.QtWidgets import QScrollBar

class CustomScrollBar(QScrollBar):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setStyleSheet("""
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 4px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #3b82f6;
                min-height: 30px;
                border-radius: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background: #2563eb;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                subcontrol-origin: margin;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
