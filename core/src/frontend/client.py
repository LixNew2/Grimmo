import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from core.src.backend.controlleurs.c_ui import login, add_user, disconnect, add_good, add_event, home_page, goods_page, set_events, tab_clicked, delete_good, delete_event, users_page, delete_user, customer_page, owner_page, add_customer, add_good_page, delete_customer, delete_owner, edit_row, get_stats
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QComboBox, QRadioButton, QStackedWidget, QFrame, QSpinBox, QCalendarWidget, QTableWidget, QTableWidgetItem, QTabWidget, QPlainTextEdit, QTimeEdit, QMessageBox, QFileDialog 
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
        self.view_user = self.findChild(QPushButton, "view_user")
        self.view_proprio = self.findChild(QPushButton, "view_proprio_2")
        self.view_customers = self.findChild(QPushButton, "view_customers")
        self.add_proprio = self.findChild(QPushButton, "add_proprio")
        self.add_customer = self.findChild(QPushButton, "add_customer")
        
        #Add Agent
        self.add_user_btn = self.findChild(QPushButton, "add_user_btn")
        self.last_name_add_user = self.findChild(QLineEdit, "last_name_add_user")
        self.first_name_add_user = self.findChild(QLineEdit, "first_name_add_user")
        self.phone_add_user = self.findChild(QLineEdit, "phone_add_user") 
        self.password_add_user = self.findChild(QLineEdit, "password_add_user")
        self.groups_add_user = self.findChild(QComboBox, "groups_add_user")
        self.error_add_agent = self.findChild(QLabel, "error_add_agent")
        self.succes_add_user = self.findChild(QLabel, "succes_add_user")
        self.email_add_user = self.findChild(QLineEdit, "email_add_user")

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
        self.btn_add_event = self.findChild(QTabWidget, 'btn_add_event')
        self.error_add_good = self.findChild(QLabel, "error_add_goods")
        self.succes_add_good = self.findChild(QLabel, "succes_add_good")
        self.succes_delete_good = self.findChild(QLabel, "delete_good_success")
        self.error_delete_good = self.findChild(QLabel, "error_delete_good")
        self.owner_combo_box = self.findChild(QComboBox, "owner_combo_box")
        self.image_btn = self.findChild(QPushButton, "image_btn")
        self.url = self.findChild(QLabel, "url")
        self.title = self.findChild(QLineEdit, "good_title")

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
        self.delete_event_btn = self.findChild(QPushButton, "delete_event_btn")
        self.succes_delete_event = self.findChild(QLabel, "delete_event_success")
        self.error_delete_event = self.findChild(QLabel, "delete_event_error")
        self.edit_event_success = self.findChild(QLabel, "edit_event_success")
        self.edit_event_error = self.findChild(QLabel, "edit_event_error")

        #Goods
        self.table = self.findChild(QTableWidget, "goods_table")
        self.delete_good_btn = self.findChild(QPushButton, "delete_good_btn")
        self.edit_good_error = self.findChild(QLabel, "edit_good_error")
        self.edit_good_success = self.findChild(QLabel, "edit_good_success")
        self.total_of_view = self.findChild(QLabel, "total_of_view")
        self.view_of_the_month = self.findChild(QLabel, "view_of_the_month")
        self.avg_view_per_month = self.findChild(QLabel, "avg_view_per_month")

        #View users
        self.user_table = self.findChild(QTableWidget, "user_table")
        self.delete_user_btn = self.findChild(QPushButton, "delete_user_btn")
        self.delete_user_success = self.findChild(QLabel, "delete_user_success")
        self.delete_user_error = self.findChild(QLabel, "delete_user_error")
        self.edit_user_success = self.findChild(QLabel, "edit_user_success")
        self.edit_user_error = self.findChild(QLabel, "edit_user_error")

        #View Customers
        self.table_customer = self.findChild(QTableWidget, "table_customer")
        self.success_customer = self.findChild(QLabel, "success_customer")
        self.error_customer = self.findChild(QLabel, "error_cutomer")
        self.delete_customer = self.findChild(QPushButton, "delete_customer")
        self.edit_customer_success = self.findChild(QLabel, "edit_customer_success")
        self.edit_customer_error = self.findChild(QLabel, "edit_customer_error")

        #View Proprio
        self.proprio_table = self.findChild(QTableWidget, "proprio_table")
        self.success_proprio = self.findChild(QLabel, "success_proprio")
        self.error_proprio = self.findChild(QLabel, "error_proprio")
        self.delete_proprio = self.findChild(QPushButton, "delete_proprio")
        self.edit_proprio_sucess = self.findChild(QLabel, "edit_proprio_sucess")
        self.proprio_edit_error = self.findChild(QLabel, "proprio_edit_error")

        #Add Customer
        self.add_customer_owner_btn = self.findChild(QPushButton, "add_customer_btn")
        self.success_add_customer = self.findChild(QLabel, "success_add_customer")
        self.phone_customer = self.findChild(QLineEdit, "phone_customer")
        self.name_customer = self.findChild(QLineEdit, "name_customer") 
        self.error_add_customer = self.findChild(QLabel, "error_add_customer") 
        self.email_customer = self.findChild(QLineEdit, "email_customer")
        self.first_name_customer = self.findChild(QLineEdit, "first_name_customer")
        self.password = self.findChild(QLineEdit, "password")

        #Actions
        self.home.clicked.connect(lambda : home_page(self.pages, self.good_table_home, self.aganda_table_home, QTableWidgetItem, self.add_user_home, self.view_user))
        self.connect_to_ldap_btn.clicked.connect(lambda : login(self.username_login.text(), self.password_login.text(), self.pages, self.username, self.menu, self.good_table_home, self.aganda_table_home, QTableWidgetItem, self.add_user_home, self.error_login, self.view_user))
        self.add_user_home.clicked.connect(lambda : self.pages.setCurrentIndex(6))
        self.view_home.clicked.connect(lambda : goods_page(self.pages, self.table, QTableWidgetItem))
        self.aganda_home.clicked.connect(lambda : self.pages.setCurrentIndex(3))
        self.add_good_home.clicked.connect(lambda : add_good_page(self.pages, self.owner_combo_box))
        self.add_user_btn.clicked.connect(lambda : add_user(self.last_name_add_user, self.first_name_add_user, self.password_add_user, self.phone_add_user, self.groups_add_user, self.error_add_agent, self.succes_add_user, self.email_add_user))
        self.disconnect_btn.clicked.connect(lambda : disconnect(self.menu, self.pages))
        self.btn_add_add_good.clicked.connect(lambda : add_good(self.city_add_good, self.street_add_good, self.postal_add_good, self.type_add_good, self.surface_add_good, self.nbr_room_add_good, self.buy_add_good, self.price_entry_add_bien, self.error_add_good, self.succes_add_good, self.owner_combo_box, self.url, self.title))
        self.buy_add_good.clicked.connect(lambda : self.month_label.hide())
        self.rental_add_good.clicked.connect(lambda : self.month_label.show())
        self.calendar.clicked.connect(self.handle_date)
        self.add_event.clicked.connect(lambda : add_event(self.calendar, self.event_hours, self.event_desc, self.event_street, self.event_cp, self.event_city, self.event_title, self.error_add_event, self.succes_add_event, QDate, QTime))
        self.btn_add_event.tabBarClicked.connect(self.set_tab_clicked)
        self.delete_good_btn.clicked.connect(lambda : delete_good(self.table, self.error_delete_good, self.succes_delete_good, QMessageBox))
        self.delete_event_btn.clicked.connect(lambda : delete_event(self.agenda_table, self.error_delete_event, self.succes_delete_event, QMessageBox))
        self.view_user.clicked.connect(lambda : users_page(self.pages, self.user_table, QTableWidgetItem))
        self.delete_user_btn.clicked.connect(lambda : delete_user(self.user_table, self.delete_user_success, self.delete_user_error, QMessageBox))
        self.add_customer.clicked.connect(lambda : self.pages.setCurrentIndex(7))
        self.view_customers.clicked.connect(lambda : customer_page(self.pages, self.table_customer, QTableWidgetItem))
        self.add_proprio.clicked.connect(lambda : self.pages.setCurrentIndex(9))
        self.view_proprio.clicked.connect(lambda : owner_page(self.pages, self.proprio_table, QTableWidgetItem))
        self.add_customer_btn.clicked.connect(lambda : add_customer(self.name_customer, self.first_name_customer, self.email_customer, self.phone_customer, self.password, self.error_add_customer, self.success_add_customer))
        self.delete_customer.clicked.connect(lambda : delete_customer(self.table_customer, self.success_customer, self.error_customer, QMessageBox))
        self.delete_proprio.clicked.connect(lambda : delete_owner(self.proprio_table, self.success_proprio, self.error_proprio, QMessageBox))
        self.table.cellChanged.connect(lambda row, column: edit_row(row, column, self.table, 0, QTableWidgetItem, self.edit_good_success, self.edit_good_error))
        self.table_customer.cellChanged.connect(lambda row, column: edit_row(row, column, self.table_customer, 1, QTableWidgetItem, self.edit_customer_success, self.edit_customer_error))
        self.proprio_table.cellChanged.connect(lambda row, column: edit_row(row, column, self.proprio_table, 2, QTableWidgetItem, self.edit_proprio_sucess,  self.proprio_edit_error))
        self.user_table.cellChanged.connect(lambda row, column: edit_row(row, column, self.user_table, 3, QTableWidgetItem, self.edit_user_success, self.edit_user_error))
        self.agenda_table.cellChanged.connect(lambda row, column: edit_row(row, column, self.agenda_table, 4, QTableWidgetItem, self.edit_event_success, self.edit_event_error, QDate))
        self.image_btn.clicked.connect(self.open_file_dialog)
        self.table.verticalHeader().sectionClicked.connect(lambda row: get_stats(row, self.avg_view_per_month, self.view_of_the_month, self.total_of_view, self.table))

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
        self.table.hideColumn(9)
        self.good_table_home.hideColumn(9)
        self.succes_delete_good.hide()
        self.error_delete_good.hide()
        self.aganda_table_home.hideColumn(7)
        self.agenda_table.hideColumn(7)
        self.succes_delete_event.hide()
        self.error_delete_event.hide()
        self.delete_user_success.hide()
        self.delete_user_error.hide()
        self.user_table.hideColumn(5)
        self.success_customer.hide()
        self.error_cutomer.hide()
        self.table_customer.hideColumn(4)
        self.success_proprio.hide()
        self.error_proprio.hide()
        self.proprio_table.hideColumn(4)
        self.success_add_customer.hide()
        self.error_add_customer.hide()
        self.success_add_proprio.hide()
        self.error_add_proprio.hide()
        self.edit_good_success.hide()
        self.edit_good_error.hide()
        self.edit_event_success.hide()
        self.edit_event_error.hide()
        self.edit_proprio_sucess.hide()
        self.proprio_edit_error.hide()
        self.edit_customer_success.hide()
        self.edit_customer_error.hide()
        self.edit_user_success.hide()
        self.edit_user_error.hide()
        self.add_proprio.hide()
        self.view_proprio.hide()

        #Show App
        self.show()

    def set_tab_clicked(self):
        global tab_clicked
        tab_clicked = self.btn_add_event.currentIndex()

    def handle_date(self, date):
        global tab_clicked
        if tab_clicked == 1:
            set_events(self.agenda_table, QTableWidgetItem, date)

    def open_file_dialog(self):
        file, _ = QFileDialog.getOpenFileName(self, "Selectionner une image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        self.url.setText(file)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI()
    sys.exit(app.exec_())