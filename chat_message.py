from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class ChatMessage(QLabel):
    def __init__(self, message, is_user=False, dark_mode=False):
        super().__init__()
        self.is_user = is_user
        self.dark_mode = dark_mode
        self.setWordWrap(True)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setMaximumWidth(420)
        self.setFont(QFont("Inter", 14))
        self.setContentsMargins(14, 10, 14, 10)
        self.setStyleSheet(self.bubble_style())
        self.setText(self.format_message(message))

    def format_message(self, message):
        import html
        escaped = html.escape(message)
        return escaped.replace("\n", "<br>")

    def bubble_style(self):
        if self.is_user:
            if self.dark_mode:
                return (
                    "background-color: #4b5563; color: white; "
                    "border-radius: 16px; padding: 14px; "
                    "margin-left: 60px; margin-top: 8px; margin-bottom: 8px; "
                    "box-shadow: 0 2px 8px rgba(75, 85, 99, 0.5);"
                )
            else:
                return (
                    "background-color: #a5f3fc; color: #0c4a6e; "
                    "border-radius: 16px; padding: 14px; "
                    "margin-left: 60px; margin-top: 8px; margin-bottom: 8px; "
                    "box-shadow: 0 2px 8px rgba(165, 243, 252, 0.6);"
                )
        else:
            if self.dark_mode:
                return (
                    "background-color: #334155; color: #e0e7ff; "
                    "border-radius: 16px; padding: 14px; "
                    "margin-right: 60px; margin-top: 8px; margin-bottom: 8px; "
                    "box-shadow: 0 2px 8px rgba(51, 65, 85, 0.7);"
                )
            else:
                return (
                    "background-color: #dbeafe; color: #1e293b; "
                    "border-radius: 16px; padding: 14px; "
                    "margin-right: 60px; margin-top: 8px; margin-bottom: 8px; "
                    "box-shadow: 0 2px 8px rgba(219, 234, 254, 0.6);"
                )
