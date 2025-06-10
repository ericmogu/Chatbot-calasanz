import sys
import json
import re
from difflib import SequenceMatcher
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QSizePolicy,
    QScrollArea, QFrame, QSpacerItem, QScrollBar
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer


class ChatbotCalasanz:
    def __init__(self, ruta_json='faq.json'):
        self.faq = self.cargar_faq(ruta_json)
        self.categorias = self.obtener_categorias()

    def cargar_faq(self, ruta_json):
        try:
            with open(ruta_json, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            return datos['faq']
        except Exception:
            print("Error al cargar el archivo JSON")
            return []

    def obtener_categorias(self):
        if not self.faq:
            return []
        return list(set(item['categoria'] for item in self.faq))

    def normalizar_texto(self, texto):
        texto = texto.lower().strip()
        texto = re.sub(r'[^\w\s]', '', texto)
        return texto

    def calcular_similitud(self, texto1, texto2):
        return SequenceMatcher(None, texto1, texto2).ratio()

    def buscar_por_palabras_clave(self, consulta_usuario):
        consulta_normalizada = self.normalizar_texto(consulta_usuario)
        palabras_consulta = set(consulta_normalizada.split())

        resultados = []

        for item in self.faq:
            palabras_clave_texto = ' '.join(item.get('palabras_clave', []))
            palabras_clave_item = set(self.normalizar_texto(palabras_clave_texto).split())
            coincidencias_clave = len(palabras_consulta.intersection(palabras_clave_item))

            pregunta_normalizada = self.normalizar_texto(item['pregunta'])
            similitud_pregunta = self.calcular_similitud(consulta_normalizada, pregunta_normalizada)

            puntuacion = coincidencias_clave * 2 + similitud_pregunta

            if puntuacion > 0.3:
                resultados.append((item, puntuacion))

        resultados.sort(key=lambda x: x[1], reverse=True)
        return resultados

    def buscar_respuesta_exacta(self, consulta_usuario):
        consulta_normalizada = self.normalizar_texto(consulta_usuario)

        for item in self.faq:
            if self.normalizar_texto(item['pregunta']) == consulta_normalizada:
                return item
        return None

    def encontrar_respuesta(self, consulta_usuario):
        respuesta_exacta = self.buscar_respuesta_exacta(consulta_usuario)
        if respuesta_exacta:
            return respuesta_exacta['respuesta'], 1.0, respuesta_exacta['categoria']

        resultados = self.buscar_por_palabras_clave(consulta_usuario)

        if resultados:
            mejor_resultado = resultados[0]
            item, puntuacion = mejor_resultado
            return item['respuesta'], puntuacion, item['categoria']

        return self.respuesta_no_encontrada(), 0.0, "general"

    def respuesta_no_encontrada(self):
        return ("Lo siento, no tengo información específica sobre esa consulta. "
                "Puedes contactar directamente al Colegio Calasanz Buenavista al "
                "teléfono 601 7920388 o visitarnos en la Carrera 17F # 77 – 75 SUR, "
                "Buenos Aires, Ciudad Bolívar.")

    def mostrar_categorias(self):
        categorias_texto = {
            'informacion_general': 'Información General',
            'ubicacion_contacto': 'Ubicación y Contacto',
            'matriculas': 'Matrículas',
            'admisiones': 'Admisiones',
            'academico': 'Información Académica',
            'horarios': 'Horarios',
            'filosofia': 'Filosofía Educativa',
            'red_colegios': 'Red de Colegios',
            'documentos': 'Documentos y Requisitos',
            'costos': 'Costos',
            'transporte': 'Transporte',
            'eventos': 'Eventos',
            'comunicacion': 'Comunicación',
            'uniforme': 'Uniforme'
        }

        texto = "\nCATEGORÍAS DISPONIBLES:\n"
        for i, categoria in enumerate(self.categorias, 1):
            nombre_categoria = categorias_texto.get(categoria, categoria.replace('_', ' ').title())
            texto += f"{i}. {nombre_categoria}\n"
        texto += "\n"
        return texto

    def procesar_consulta(self, consulta_usuario):
        if consulta_usuario.lower() in ['help', 'ayuda', 'categorias']:
            return self.mostrar_categorias()

        respuesta, puntuacion, categoria = self.encontrar_respuesta(consulta_usuario)

        if puntuacion >= 0.8:
            return respuesta
        elif puntuacion >= 0.5:
            return f"{respuesta}\n\n(Si necesitas información más específica, contacta al colegio)"
        elif puntuacion > 0:
            return f"{respuesta}\n\nTambién puedes escribir 'ayuda' para ver todas las categorías disponibles"
        else:
            return respuesta


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


def main():
    app = QApplication(sys.argv)
    chatbot_window = ChatbotApp()
    chatbot_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
