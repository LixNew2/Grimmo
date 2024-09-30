import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from core.src.backend.controlleurs.c_ui import login
import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QPushButton, QLineEdit, QLabel, QComboBox, QMenuBar, QMenu, QRadioButton, QStackedWidget
from PyQt5 import uic

#Class
class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        #Load File gui
        uic.loadUi("core/GUI/interface.ui", self)

        #Widgets
        self.connect_to_ldap_btn = self.findChild(QPushButton, "btn_connection")
        self.username_line_edit = self.findChild(QLineEdit, "lineEdit_name")
        self.password_line_edit = self.findChild(QLineEdit, "lineEdit_password")
        self.pages = self.findChild(QStackedWidget, "stackedWidget")  

        #Actions
        self.connect_to_ldap_btn.clicked.connect(lambda : login(self.username_line_edit.text(), self.password_line_edit.text(), self.pages))

        #Show App
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI()
    sys.exit(app.exec_())