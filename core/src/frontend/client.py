import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from core.src.backend.controlleurs.c_ui import login, add_user, disconnect, add_good, add_event, show_event
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QComboBox, QRadioButton, QStackedWidget, QFrame, QSpinBox, QCalendarWidget
from PyQt5 import uic

#Class
class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        #Load File gui
        uic.loadUi("core/GUI/interface.ui", self)

        #Widgets
        self.pages = self.findChild(QStackedWidget, "pages")  
        self.username = self.findChild(QLabel, "username")
        self.home = self.findChild(QPushButton, "home_home")
        self.menu = self.findChild(QFrame, "top_menu")
        self.disconnect_btn = self.findChild(QPushButton, "disconnect")
        
        self.connect_to_ldap_btn = self.findChild(QPushButton, "connect_login")
        self.username_login = self.findChild(QLineEdit, "username_login")
        self.password_login = self.findChild(QLineEdit, "password_login")

        self.add_user_home = self.findChild(QPushButton, "add_user_home")
        self.view_home = self.findChild(QPushButton, "view_home")
        self.aganda_home = self.findChild(QPushButton, "agenda")
        self.add_good_home = self.findChild(QPushButton, "add_good")
        
        self.add_user_btn = self.findChild(QPushButton, "add_user_btn")
        self.last_name_add_user = self.findChild(QLineEdit, "last_name_add_user")
        self.first_name_add_user = self.findChild(QLineEdit, "first_name_add_user")
        self.phone_add_user = self.findChild(QLineEdit, "phone_add_user") 
        self.password_add_user = self.findChild(QLineEdit, "password_add_user")
        self.groups_add_user = self.findChild(QComboBox, "groups_add_user")

        self.city_add_good = self.findChild(QLineEdit,"add_ville_add_bien")
        self.street_add_good = self.findChild(QLineEdit,"add_rue_add_bien")
        self.postal_add_good = self.findChild(QLineEdit,"add_postal_add_bien")
        self.type_add_good = self.findChild(QComboBox,"add_type_add_bien")
        self.surface_add_good = self.findChild(QSpinBox, "add_surface_add_bien")
        self.nbr_room_add_good = self.findChild(QSpinBox, "nbr_room_add_bien")
        self.rental_add_good = self.findChild(QRadioButton,"location_add_bien")
        self.buy_add_good = self.findChild(QRadioButton, "acheter_add_bien")
        self.price_entry_add_bien = self.findChild(QSpinBox, "price_entry_add_bien")
        self.btn_add_add_good = self.findChild(QPushButton,"btn_add_bien")
        self.month_label = self.findChild(QLabel, "mois_label")

        self.calendar = self.findChild(QCalendarWidget, "calendar")
        self.event_title = self.findChild(QLabel, "calendar_title")
        self.event_street = self.findChild(QLabel, "calendar_street")
        self.event_city = self.findChild(QLabel, "calendar_city")
        self.event_hours = self.findChild(QLabel, "calendar_hours")
        self.event_cp = self.findChild(QLabel, "calendar_cp")

        #Actions
        self.home.clicked.connect(lambda : self.pages.setCurrentIndex(1))
        self.connect_to_ldap_btn.clicked.connect(lambda : login(self.username_login.text(), self.password_login.text(), self.pages, self.username, self.menu))
        self.add_user_home.clicked.connect(lambda : self.pages.setCurrentIndex(5))
        self.view_home.clicked.connect(lambda : self.pages.setCurrentIndex(4))
        self.aganda_home.clicked.connect(lambda : self.pages.setCurrentIndex(3))
        self.add_good_home.clicked.connect(lambda : self.pages.setCurrentIndex(2))
        self.add_user_btn.clicked.connect(lambda : add_user(self.last_name_add_user.text(), self.first_name_add_user.text(), self.password_add_user.text(), self.phone_add_user.text(), self.groups_add_user.currentText()))
        self.disconnect_btn.clicked.connect(lambda : disconnect(self.menu, self.pages))
        self.btn_add_add_good.clicked.connect(lambda : add_good(self.city_add_good.text(), self.street_add_good.text(), self.postal_add_good.text(), self.type_add_good.currentText(), self.surface_add_good.value(), self.nbr_room_add_good.value(), 1 if self.buy_add_good.isChecked() else 0, self.price_entry_add_bien.value()))
        self.buy_add_good.clicked.connect(lambda : self.month_label.hide())
        self.rental_add_good.clicked.connect(lambda : self.month_label.show())
        self.calendar.clicked.connect(self.handle_date)
        
        #Display
        self.menu.hide()
        self.pages.setCurrentIndex(0)
        self.month_label.hide()

        #Show App
        self.show()

    #Bug : 
    def handle_date(self, date):
        show_event(date, self.event_title, self.event_street, self.event_city, self.event_hours, self.event_cp)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI()
    sys.exit(app.exec_())