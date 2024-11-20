import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from core.src.backend.controlleurs.c_ui import login, add_user, disconnect, add_good, add_event, home_page, goods_page, set_events, tab_clicked
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QComboBox, QRadioButton, QStackedWidget, QFrame, QSpinBox, QCalendarWidget, QTableWidget, QTableWidgetItem, QTabWidget, QPlainTextEdit, QTimeEdit
from PyQt5 import uic
from PyQt5.QtCore import QTime, QDate

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
        
        #Login
        self.connect_to_ldap_btn = self.findChild(QPushButton, "connect_login")
        self.username_login = self.findChild(QLineEdit, "username_login")
        self.password_login = self.findChild(QLineEdit, "password_login")
        self.error_login = self.findChild(QLabel, "error")

        #Home
        self.add_user_home = self.findChild(QPushButton, "add_user_home")
        self.view_home = self.findChild(QPushButton, "view_home")
        self.aganda_home = self.findChild(QPushButton, "agenda")
        self.add_good_home = self.findChild(QPushButton, "add_good")
        self.good_table_home = self.findChild(QTableWidget, "good_table_home")
        self.aganda_table_home = self.findChild(QTableWidget, "aganda_table_home")
        
        #Add Agent
        self.add_user_btn = self.findChild(QPushButton, "add_user_btn")
        self.last_name_add_user = self.findChild(QLineEdit, "last_name_add_user")
        self.first_name_add_user = self.findChild(QLineEdit, "first_name_add_user")
        self.phone_add_user = self.findChild(QLineEdit, "phone_add_user") 
        self.password_add_user = self.findChild(QLineEdit, "password_add_user")
        self.groups_add_user = self.findChild(QComboBox, "groups_add_user")
        self.error_add_agent = self.findChild(QLabel, "error_add_agent")
        self.succes_add_user = self.findChild(QLabel, "succes_add_user")

        #Add Good
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
        self.table = self.findChild(QTableWidget, "goods_table")
        self.btn_add_event = self.findChild(QTabWidget, 'btn_add_event')
        self.error_add_good = self.findChild(QLabel, "error_add_goods")
        self.succes_add_good = self.findChild(QLabel, "succes_add_good")

        #Calendar
        self.calendar = self.findChild(QCalendarWidget, "calendar")
        self.event_title = self.findChild(QLineEdit, "calendar_title")
        self.event_street = self.findChild(QLineEdit, "calendar_street")
        self.event_city = self.findChild(QLineEdit, "calendar_city")
        self.event_hours = self.findChild(QTimeEdit, "calendar_hours")
        self.event_cp = self.findChild(QLineEdit, "calendar_cp")
        self.event_desc = self.findChild(QPlainTextEdit, "add_description_event")
        self.agenda_table = self.findChild(QTableWidget, "agenda_table")
        self.add_event = self.findChild(QPushButton,"add_event")
        self.error_add_event = self.findChild(QLabel, "error_add_event")
        self.succes_add_event = self.findChild(QLabel, "succes_add_event")

        #Actions
        self.home.clicked.connect(lambda : home_page(self.pages, self.good_table_home, self.aganda_table_home, QTableWidgetItem, self.add_user_home))
        self.connect_to_ldap_btn.clicked.connect(lambda : login(self.username_login.text(), self.password_login.text(), self.pages, self.username, self.menu, self.good_table_home, self.aganda_table_home, QTableWidgetItem, self.add_user_home, self.error_login))
        self.add_user_home.clicked.connect(lambda : self.pages.setCurrentIndex(5))
        self.view_home.clicked.connect(lambda : goods_page(self.pages, self.table, QTableWidgetItem))
        self.aganda_home.clicked.connect(lambda : self.pages.setCurrentIndex(3))
        self.add_good_home.clicked.connect(lambda : self.pages.setCurrentIndex(2))
        self.add_user_btn.clicked.connect(lambda : add_user(self.last_name_add_user, self.first_name_add_user, self.password_add_user, self.phone_add_user, self.groups_add_user, self.error_add_agent, self.succes_add_user))
        self.disconnect_btn.clicked.connect(lambda : disconnect(self.menu, self.pages))
        self.btn_add_add_good.clicked.connect(lambda : add_good(self.city_add_good, self.street_add_good, self.postal_add_good, self.type_add_good, self.surface_add_good, self.nbr_room_add_good, self.buy_add_good, self.price_entry_add_bien, self.error_add_good, self.succes_add_good))
        self.buy_add_good.clicked.connect(lambda : self.month_label.hide())
        self.rental_add_good.clicked.connect(lambda : self.month_label.show())
        self.calendar.clicked.connect(self.handle_date)
        self.add_event.clicked.connect(lambda : add_event(self.calendar, self.event_hours, self.event_desc, self.event_street, self.event_cp, self.event_city, self.event_title, self.error_add_event, self.succes_add_event, QDate, QTime))
        self.btn_add_event.tabBarClicked.connect(self.set_tab_clicked)

        #Display
        self.menu.hide()
        self.pages.setCurrentIndex(0)
        self.month_label.hide()
        self.error_login.hide()
        self.error_add_agent.hide()
        self.error_add_event.hide()
        self.error_add_good.hide()
        self.succes_add_user.hide()
        self.succes_add_good.hide()
        self.succes_add_event.hide()

        #Show App
        self.show()

    def set_tab_clicked(self):
        global tab_clicked
        tab_clicked = self.btn_add_event.currentIndex()

    def handle_date(self, date):
        global tab_clicked
        if tab_clicked == 1:
            set_events(self.agenda_table, QTableWidgetItem, date)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI()
    sys.exit(app.exec_())