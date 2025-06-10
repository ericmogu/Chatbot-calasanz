from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QSizePolicy, QScrollArea, QFrame, QSpacerItem
from PyQt5.QtCore import Qt, QTimer
from chatbot import ChatbotCalasanz
from chat_message import ChatMessage
from custom_scrollbar import CustomScrollBar

class ChatbotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.dark_mode = False
        self.chatbot = ChatbotCalasanz('faq.json')
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Chatbot Colegio Calasanz')
        self.setGeometry(100, 100, 700, 720)
        self.setup_styles()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(48, 48, 48, 48)
        main_layout.setSpacing(24)

        header_layout = QHBoxLayout()
        self.titleLabel = QLabel("Chatbot Colegio Calasanz")
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header_layout.addWidget(self.titleLabel)

        self.theme_toggle = QPushButton()
        self.theme_toggle.setCheckable(True)
        self.theme_toggle.setFixedSize(60, 60)
        self.update_theme_icon()
        self.theme_toggle.setToolTip("Cambiar modo claro/oscuro")
        self.theme_toggle.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_toggle, alignment=Qt.AlignRight)

        main_layout.addLayout(header_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setVerticalScrollBar(CustomScrollBar(Qt.Vertical, self.scroll_area))
        main_layout.addWidget(self.scroll_area)

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_container.setLayout(self.chat_layout)
        self.scroll_area.setWidget(self.chat_container)

        input_layout = QHBoxLayout()
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Escribe tu consulta aquí...")
        self.text_input.returnPressed.connect(self.send_query)
        input_layout.addWidget(self.text_input)

        self.send_button = QPushButton("Enviar")
        self.send_button.clicked.connect(self.send_query)
        input_layout.addWidget(self.send_button)

        main_layout.addLayout(input_layout)

        self.setLayout(main_layout)

        self.add_message(
            "Hola! Soy el asistente virtual del Colegio Calasanz Buenavista.\n"
            "Puedo ayudarte con información sobre matrículas, admisiones, ubicación y más.\n"
            "Escribe 'ayuda' para ver las categorías disponibles.\n"
            "Escribe 'salir' para terminar.", is_user=False)

    def setup_styles(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QWidget {
                    background-color: #0f172a;
                    font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    color: #e0e7ff;
                }
                QLabel#titleLabel {
                    font-size: 48px;
                    font-weight: 700;
                    color: #f1f5f9;
                    padding-bottom: 20px;
                }
                QLineEdit {
                    border-radius: 14px;
                    border: 1.5px solid #475569;
                    padding: 14px;
                    font-size: 18px;
                    color: #e0e7ff;
                    background-color: #1e293b;
                    transition: border-color 0.3s ease;
                }
                QLineEdit:focus {
                    border-color: #3b82f6;
                    background-color: #334155;
                }
                QPushButton {
                    background-color: #3b82f6;
                    color: #f8fafc;
                    border-radius: 14px;
                    padding: 14px;
                    font-weight: 700;
                    font-size: 18px;
                    min-width: 140px;
                    margin-left: 12px;
                    transition: background-color 0.3s ease;
                }
                QPushButton:hover {
                    background-color: #2563eb;
                }
                QScrollArea {
                    border: none;
                }
                QPushButton#themeToggle {
                    background: transparent;
                    border: none;
                    font-size: 28px;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #ffffff;
                    font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    color: #475569;
                }
                QLabel#titleLabel {
                    font-size: 48px;
                    font-weight: 700;
                    color: #0f172a;
                    padding-bottom: 20px;
                }
                QLineEdit {
                    border-radius: 14px;
                    border: 1.5px solid #cbd5e1;
                    padding: 14px;
                    font-size: 18px;
                    color: #334155;
                    background-color: #f8fafc;
                    transition: border-color 0.3s ease;
                }
                QLineEdit:focus {
                    border-color: #3b82f6;
                    background-color: #ffffff;
                }
                QPushButton {
                    background-color: #0f172a;
                    color: #f8fafc;
                    border-radius: 14px;
                    padding: 14px;
                    font-weight: 700;
                    font-size: 18px;
                    min-width: 140px;
                    margin-left: 12px;
                    transition: background-color 0.3s ease;
                }
                QPushButton:hover {
                    background-color: #3b82f6;
                }
                QScrollArea {
                    border: none;
                }
                QPushButton#themeToggle {
                    background: transparent;
                    border: none;
                    font-size: 28px;
                }
            """)

    def update_theme_icon(self):
        if self.dark_mode:
            self.theme_toggle.setText("☀️")
            self.theme_toggle.setToolTip("Cambiar a modo claro")
        else:
            self.theme_toggle.setText("🌙")
            self.theme_toggle.setToolTip("Cambiar a modo oscuro")
        self.theme_toggle.setObjectName("themeToggle")
        self.theme_toggle.setStyleSheet("font-size: 28px; background: transparent; border: none;")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.setup_styles()
        self.update_theme_icon()
        self.reload_messages_style()

    def reload_messages_style(self):
        for i in range(self.chat_layout.count()):
            item = self.chat_layout.itemAt(i)
            if item is not None:
                h_layout = item.layout()
                if h_layout is not None:
                    for j in range(h_layout.count()):
                        widget = h_layout.itemAt(j).widget()
                        if isinstance(widget, ChatMessage):
                            widget.dark_mode = self.dark_mode
                            widget.setStyleSheet(widget.bubble_style())

    def add_message(self, message, is_user=False):
        message_widget = ChatMessage(message, is_user=is_user, dark_mode=self.dark_mode)
        h_layout = QHBoxLayout()
        if is_user:
            spacer = QSpacerItem(40, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
            h_layout.addItem(spacer)
            h_layout.addWidget(message_widget)
        else:
            h_layout.addWidget(message_widget)
            spacer = QSpacerItem(40, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
            h_layout.addItem(spacer)
        self.chat_layout.addLayout(h_layout)

        # Auto-scroll to bottom after the UI has updated
        QTimer.singleShot(10, self.scroll_to_bottom)  # Ajustar el tiempo a 10 ms

    def scroll_to_bottom(self):
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def send_query(self):
        user_query = self.text_input.text().strip()
        if not user_query:
            return
        if user_query.lower() in {'salir', 'exit', 'quit', 'bye'}:
            self.add_message("Hasta luego! Gracias por usar el chatbot del Colegio Calasanz Buenavista.", is_user=False)
            self.text_input.setDisabled(True)
            self.send_button.setDisabled(True)
            return

        self.add_message(user_query, is_user=True)
        respuesta = self.chatbot.procesar_consulta(user_query)
        self.add_message(respuesta, is_user=False)
        self.text_input.clear()

    def closeEvent(self, event):
        # Es correcto cerrar la aplicación sin problemas
        QApplication.quit()
        event.accept()
