from core.src.backend.classes.models.LDAPServer import LDAPServer
from core.src.backend.classes.models.Database import Database
from core.src.backend.config.config import CONFIG
from PrivateCode import private
from core.src.backend.classes.User import User

import uuid, time, threading
from uuid import UUID

ldap_server = LDAPServer(CONFIG["LDAP"]["ldap_url"],
                    int(CONFIG["LDAP"]["ldap_port"]),
                    CONFIG["LDAP"]["ldap_domain"],
                    CONFIG["LDAP"]["ldap_base"])
database : Database
user : User

tab_clicked = 1

@private
def _generate_uuid4() -> UUID:
    return uuid.uuid4()

@private
def _check_user_groups(search) -> bool:
    for group in user.groups:
        if group == search:
            return True
    return False

@private
def _add_user_to_ad(last_name, first_name, password, gp_name, uuid4) -> bool:
    return ldap_server.add_user(last_name, first_name, password, gp_name, uuid4)

@private
def _add_user_to_db(uuid4, last_name, first_name, phone, type, password) -> bool :
    user_id = f"{first_name[0].upper()}{last_name[0].upper()}{last_name[1:].lower()}"

    if type == 0:
        query = f"CREATE USER {user_id} WITH PASSWORD '{password}'; GRANT INSERT, UPDATE, DELETE ON TABLE EVENT, BIENS TO {user_id};"
    else:
        query = f"CREATE USER {user_id} WITH PASSWORD '{password}'; GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {user_id}; ALTER USER {user_id} WITH SUPERUSER;"
    
    result = database.query(query)
    if result[0]:
        query = f"INSERT INTO USERS VALUES ('{uuid4}', '{last_name}', '{first_name}', '{phone}', '{type}', '{user_id}');"
        return database.query(query)[0]
    else:
        print(result[1])


def add_user(last_name, first_name, password, phone, gp_name, error, success) -> bool :
    if last_name.text() == "" or first_name.text() == "" or password.text() == "" or phone.text() == "" or gp_name.currentText() == "":
        handle_message(error)
        return False
    
    if user.type_u == 0:
        uuid4 = str(_generate_uuid4())
        if _add_user_to_ad(last_name.text(), first_name.text(), password.text(), gp_name.currentText(), uuid4):
            if _add_user_to_db(uuid4, last_name.text(), first_name.text(), phone.text(), 0 if gp_name.currentText() == "Responsable" else 1, password.text()):
                handle_message(success)
                last_name.setText("")
                first_name.setText("")
                password.setText("")
                phone.setText("")
                return True
    return False

def disconnect(menu, pages):
    global ldap_server, database, user
    ldap_server.disconnect()
    database.disconnect()
    menu.hide()
    pages.setCurrentIndex(0)
    database = None
    user = None

def add_good(city, address, cp, type_good, surface, nbr_room, commendable_purshasable, price, error, success) -> bool:
    """
    If buy is checked commendable_purshasable = 1
    If rent is checked commendable_purshasable = 0
    """
    global user

    if city.text() == "" or address.text() == "" or cp.text() == "" or type_good.currentText() == "" or nbr_room.value() == 0 or surface.value() == 0 or price.value() == 0:
        handle_message(error)
        return False

    if type_good.currentText() == "Appartement":
        type_good = 0
    elif type_good.currentText() == "Maison":
        type_good = 1
    else:
        type_good = 2 #Terrain

    uuid4 = str(_generate_uuid4())
    query = f"INSERT INTO BIENS VALUES ('{uuid4}', '{address.text()}', '{city.text()}', '{cp.text()}', {type_good}, {surface.value()}, {nbr_room.value()}, {price.value()}, {1 if commendable_purshasable.isChecked() else 0}, '{user.uid}');"
    handle_message(success)
    city.setText("")
    address.setText("")
    cp.setText("")
    surface.setValue(0)
    nbr_room.setValue(0)
    price.setValue(0)
    return database.query(query)[0]

@private
def get_goods():
    if user.type_u == 0:
        query = "SELECT * FROM BIENS;"
    else:
        query = f"SELECT * FROM BIENS WHERE BIENS.uid_user = '{user.uid}';"

    result  = database.query(query)
    
    if result[0]:
        values = result[1].fetchall()
        return values


def add_event(date, hours, desc, street, cp, city, title, error, success, QDate, QTime): 
    if (date.selectedDate() == None or hours.time() == None or desc.toPlainText() == "" or street.text() == "" or cp.text() == "" or city.text() == "" or title.text() == ""):
        handle_message(error)
        return False
    
    uuid4 = str(_generate_uuid4())
    query = f"INSERT INTO EVENT VALUES ('{uuid4}', '{date.selectedDate().toString('dd/MM/yyyy')}', '{hours.time().toString('HH:mm')}', '{desc.toPlainText()}', '{street.text()}', '{cp.text()}', '{city.text()}', '{title.text()}', '{user.uid}');"
    handle_message(success)
    date.setSelectedDate(QDate())
    hours.setTime(QTime(0, 0))
    desc.setPlainText("")
    street.setText("")
    cp.setText("")
    city.setText("")
    title.setText("")
    return database.query(query)[0]

@private
def get_events(date = None) -> None:
    if date == None:
        if user.type_u == 0:
            query = f"SELECT * FROM EVENT;"
        else:
            query = f"SELECT * FROM EVENT WHERE EVENT.uid_user = '{user.uid}';"
        result = database.query(query)
        
        if result[0]:
            return result[1].fetchall()
    else:
        selected_date = date.toString("dd/MM/yyyy")
        if user.type_u == 0:
            print("ok")
            query = f"SELECT * FROM EVENT WHERE EVENT.date_event = '{selected_date}'"
        else:
            print("ok")
            query = f"SELECT * FROM EVENT WHERE EVENT.date_event = '{selected_date}' AND EVENT.uid_user = '{user.uid}';"
        
        result = database.query(query)

        if result[0]:
            return result[1].fetchall()

def set_events(table, QTableWidgetItem, date = None) -> None:
    table.setRowCount(0)

    if date == None:
        events = get_events()
    else:
        events = get_events(date)

    print(events)
    if events == None or events == []:
        return
    
    if len(events) == 0:
        return
    
    n_column = len(events[0]) 
    n_row = len(events)

    table.setRowCount(n_row)
    table.setColumnCount(n_column-1)

    i_row = -1
    i_column = -1

    for event in events:
        i_row += 1
        i_column = -1 
        print(event)
        for column in event:
            if event.index(column) == 0:
                table.setItem(i_row, 7, QTableWidgetItem(str(column)))
                continue

            i_column += 1

            table.setItem(i_row, i_column, QTableWidgetItem(str(column)))

            if i_column == 6:
                break

def home_page(pages, table1, table2, QTableWidgetItem, add_user_home, view_user):
    if user.type_u == 1: 
        add_user_home.hide()
        view_user.hide()
    else:
        add_user_home.show()
        view_user.show()

    pages.setCurrentIndex(1)
    set_goods(table1, QTableWidgetItem)
    set_events(table2, QTableWidgetItem)

def goods_page(pages, table, QTableWidgetItem):
    pages.setCurrentIndex(4)
    set_goods(table, QTableWidgetItem)

def set_goods(table, QTableWidgetItem):
    goods = get_goods()

    if goods == None or goods == []:
        return

    n_column = len(goods[0]) 
    n_row = len(goods)

    table.setRowCount(n_row)
    table.setColumnCount(n_column-1)

    i_row = -1
    i_column = -1

    for good in goods:
        i_row += 1
        i_column = -1
        for column in good:
            if good.index(column) == 0: 
                table.setItem(i_row, 8, QTableWidgetItem(str(column)))
                continue
            
            i_column += 1
           
            if i_column == 3:
                if column == 0:
                    column = "Appartement"
                elif column == 1:
                    column = "Maison"
                else:
                    column = "Terrain"
            
            if i_column == 7:
                if column == 0:
                    column = "Location"
                else:
                    column = "Achetable"

            table.setItem(i_row, i_column, QTableWidgetItem(str(column)))

            if i_column == 7:
                break

def login(LDAP_CNUSER, LDAP_PASSWORD, pages, username, menu, table1, table2, QTableWidgetItem, add_user_home, error, view_user) -> bool:
    #Init the LDAP server
    global ldap_server, user, database
    #Try to login
    if ldap_server.login(LDAP_CNUSER, LDAP_PASSWORD):     
        #Get user data
        groups = ldap_server.get_groups(LDAP_CNUSER)
        uid = ldap_server.get_uid(LDAP_CNUSER)
        
        user = User(LDAP_CNUSER, groups, uid, None, None, None, 1)

        """last_name, first_name = LDAP_CNUSER.split(" ")
        user_id = f"{first_name[0]}{last_name}"
        print(user_id)"""
        
        print(LDAP_CNUSER, LDAP_PASSWORD)
        #Init the database
        database = Database(CONFIG["POSTGRES"]["host"],
            CONFIG["POSTGRES"]["database"],
            LDAP_CNUSER.lower(),
            LDAP_PASSWORD)
            
        #Try to connect to databse
        if database.connect():
            print("Connected to the Database")
            if uid:
                result = database.query(f"SELECT last_name, first_name, phone, type_user FROM USERS WHERE USERS.uid_user = '{uid}';")
                print(result[1])
                if result[0]:
                    values = result[1].fetchall()
                    print(values)
                    user.last_name = values[0][0]
                    user.first_name = values[0][1]
                    user.phone = values[0][2]
                    user.type_u = values[0][3]
            #Display success
            """display success"""
        else:
            print("An error occured while connecting to the Database")
            return False
    else:
        #Display error
        print("no")
        handle_message(error)
        return False
    
    menu.show()
    username.setText(user.first_name + " " + user.last_name)
    home_page(pages, table1, table2, QTableWidgetItem, add_user_home, view_user)
    print("UID : ", user.uid)
    print("Groups : ", str(user.groups))
    print("CN : ", user.cn)
    print("Last Name : ", user.last_name)
    print("First Name : ", user.first_name)
    print("Phone : ", user.phone)
    print("Type : ", str(user.type_u))
    return True

def handle_message(message):
    thread = threading.Thread(target=display_message, args=(message,))
    thread.start()

def display_message(message):   
    message.show()
    time.sleep(3)
    message.hide()

def delete_good(table, error, success, QMessageBox):
    selected_item = table.currentRow()

    if selected_item == -1:
        handle_message(error)
        return
    
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Êtes-vous sur de vouloir supprimer ce bien ?")
    msg.setWindowTitle("Suppression de bien")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    reponse_msg = msg.exec_()

    if reponse_msg == QMessageBox.Cancel:
        return
    
    uuid4 = table.item(selected_item, 8).text()

    query = f"DELETE FROM BIENS WHERE BIENS.id_bien = '{uuid4}';"
    result = database.query(query)
    if result[0]:
        table.removeRow(selected_item)
        handle_message(success)
    else:
        print(result[1])

def delete_event(table, error, success, QMessageBox):
    selected_item = table.currentRow()

    if selected_item == -1:
        handle_message(error)
        return
    
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Êtes-vous sur de vouloir supprimer cet événement ?")
    msg.setWindowTitle("Suppression d'événement")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    reponse_msg = msg.exec_()

    if reponse_msg == QMessageBox.Cancel:
        return

    uuid4 = table.item(selected_item, 7).text()

    query = f"DELETE FROM EVENT WHERE EVENT.id_event = '{uuid4}';"
    result = database.query(query)
    if result[0]:
        table.removeRow(selected_item)
        handle_message(success)
    else:
        print(result[1])


def get_user():
    query = ""
    if user.type_u == 0:
        query = "SELECT * FROM USERS;"

    result  = database.query(query)
    
    if result[0]:
        values = result[1].fetchall()
        return values
    
def set_user(table, QTableWidgetItem):
    table.setRowCount(0)

    users = get_user()

    if users == None or users == [] or len(users) == 0:
        return

    
    n_column = len(users[0]) 
    n_row = len(users)

    table.setRowCount(n_row)
    table.setColumnCount(n_column)

    i_row = -1
    i_column = -1

    for user in users:
        i_row += 1
        i_column = -1 
        print(user)
        for column in user:
            if user.index(column) == 0:
                table.setItem(i_row, 5, QTableWidgetItem(str(column)))
                continue

            i_column += 1


            if i_column == 3:
                if column == 1:
                    column = "Agent"
                else :
                    column = "Responsable"
        
            table.setItem(i_row, i_column, QTableWidgetItem(str(column)))


def users_page(pages, table, QTableWidgetItem):
    pages.setCurrentIndex(5)
    set_user(table, QTableWidgetItem)

def delete_user(table, success, error, QMessageBox):
    selected_item = table.currentRow()

    if selected_item == -1:
        handle_message(error)
        return
    
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText("Êtes-vous sur de vouloir supprimer cet utilisateur ?")
    msg.setWindowTitle("Suppression d'un utilisateur")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    reponse_msg = msg.exec_()

    if reponse_msg == QMessageBox.Cancel:
        return
    
    uuid4 = table.item(selected_item, 5).text()

    if(ldap_server.delete_user(table.item(selected_item, 4).text())):
        query = f"DELETE FROM USERS WHERE USERS.uid_user = '{uuid4}'; REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM {table.item(selected_item, 4).text()}; DROP USER {table.item(selected_item, 4).text()};"
        result = database.query(query)
        if result[0]:
            table.removeRow(selected_item)
            handle_message(success)