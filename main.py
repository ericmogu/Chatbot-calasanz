import sys
from PyQt5.QtWidgets import QApplication
from chatbot_app import ChatbotApp

def main():
    app = QApplication(sys.argv)
    chatbot_window = ChatbotApp()
    chatbot_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
