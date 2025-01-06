from core.src.backend.classes.models.LDAPServer import LDAPServer
from core.src.backend.classes.models.Database import Database
from core.src.backend.config.config import CONFIG
from PrivateCode import private
from core.src.backend.classes.User import User

import uuid, time, threading, requests, base64, json, datetime
from uuid import UUID

ldap_server = LDAPServer(CONFIG["LDAP"]["ldap_url"],
                    int(CONFIG["LDAP"]["ldap_port"]),
                    CONFIG["LDAP"]["ldap_domain"],
                    CONFIG["LDAP"]["ldap_base"])
database : Database
user : User

API = CONFIG["API"]["url"]

tab_clicked = 1
loading = False


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
def _add_user_to_db(uuid4, last_name, first_name, phone, type, password, email) -> bool :
    user_id = f"{first_name[0].upper()}{last_name[0].upper()}{last_name[1:].lower()}"

    """if type == 0:
        query = f"CREATE USER {user_id} WITH PASSWORD '{password}'; ALTER USER {user_id} WITH SUPERUSER;"
    else:
        query = f"CREATE USER {user_id} WITH PASSWORD '{password}'; GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE EVENT, BIENS, CLIENT, PROPRIETAIRE, USERS, SUPERVISER TO {user_id};

    result = database.query(query)
    if result[0]:"""
    
    data = {
        "uuid4":uuid4,
        "last_name":last_name,
        "first_name":first_name,
        "email":email,
        "phone":phone,
        "password":password,
        "type":3,
    }

    result = requests.post(f"{API}add_user", json=data, headers={'Authorization': f'Bearer {user.access_token}','Content-Type': 'application/json'})
    print(result.text)
    
    if result.status_code == 200:
        data = json.loads(result.text)
        query = f"INSERT INTO USERS VALUES ('{uuid4}', '{last_name}', '{first_name}', '{phone}', '{type}', '{user_id}', '{data['bearer']}', '{email}');"
        return database.query(query)[0]

def add_user(last_name, first_name, password, phone, gp_name, error, success, email) -> bool :
    if last_name.text() == "" or first_name.text() == "" or password.text() == "" or phone.text() == "" or gp_name.currentText() == "":
        handle_message(error)
        return False
    
    if user.type_u == 0:
        uuid4 = str(_generate_uuid4())
        if _add_user_to_ad(last_name.text(), first_name.text(), password.text(), gp_name.currentText(), uuid4):
            if _add_user_to_db(uuid4, last_name.text(), first_name.text(), phone.text(), 0 if gp_name.currentText() == "Responsable" else 1, password.text(), email.text()):
                handle_message(success)
                last_name.setText("")
                first_name.setText("")
                password.setText("")
                phone.setText("")
                email.setText("")
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

def add_good(city, address, cp, type_good, surface, nbr_room, commendable_purshasable, price, error, success, combo, url, title) -> bool:
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

    img_bytes = "null"

    if(url.text() != ""):
        with open(url.text(), 'rb') as b:
            img_bytes = base64.b64encode(b.read()).decode('utf-8')

    data = {"uuid":uuid4,
            "address":address.text(),
            "city":city.text(),
            "cp":int(cp.text()),
            "type_good":type_good,
            "surface":surface.value(),
            "nbr_room":nbr_room.value(),
            "price":price.value(),
            "commendable_purshasable":1 if commendable_purshasable.isChecked() else 0,
            "uid_client":combo.itemData(combo.currentIndex()),
            "img":img_bytes,
            'titre':title.text()
        }
    
    result = requests.post(f"{API}add_good", json=data, headers={'Authorization': f'Bearer {user.access_token}','Content-Type': 'application/json'})
    print(result.text)
    print(result.status_code)
    
    if result.status_code == 200:
        query = f"INSERT INTO BIENS VALUES ('{uuid4}', '{address.text()}', '{city.text()}', '{cp.text()}', {type_good}, {surface.value()}, {nbr_room.value()}, {price.value()}, {1 if commendable_purshasable.isChecked() else 0}, '{combo.itemData(combo.currentIndex())}', '{user.uid}');"
        handle_message(success)
        city.setText("")
        address.setText("")
        cp.setText("")
        surface.setValue(0)
        nbr_room.setValue(0)
        price.setValue(0)
        url.setText("")
        title.setText("")
        result = database.query(query)
        print(result[1])
        
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
    global loading
    loading = True
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
        for column in event:
            if event.index(column) == 0:
                table.setItem(i_row, 7, QTableWidgetItem(str(column)))
                continue

            i_column += 1

            table.setItem(i_row, i_column, QTableWidgetItem(str(column)))

            if i_column == 6:
                break

    loading = False

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
    global loading
    loading = True
    table.setRowCount(0)

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
                table.setItem(i_row, 9, QTableWidgetItem(str(column)))
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

            if i_column == 8:
                query = F"SELECT nom, prenom FROM CLIENT WHERE CLIENT.uid_proprio = '{column}';"
                result = database.query(query)
                if result[0]:
                    values = result[1].fetchall()[0]
                    column = values[0] + " " + values[1]

            table.setItem(i_row, i_column, QTableWidgetItem(str(column)))

            if i_column == 8:
                break

    loading = False 

def login(LDAP_CNUSER, LDAP_PASSWORD, pages, username, menu, table1, table2, QTableWidgetItem, add_user_home, error, view_user) -> bool:
    #Init the LDAP server
    global ldap_server, user, database
    #Try to login
    if ldap_server.login(LDAP_CNUSER, LDAP_PASSWORD):     
        #Get user data
        groups = ldap_server.get_groups(LDAP_CNUSER)
        uid = ldap_server.get_uid(LDAP_CNUSER)
        
        user = User(LDAP_CNUSER, groups, uid, None, None, None, 1, None)

        """last_name, first_name = LDAP_CNUSER.split(" ")
        user_id = f"{first_name[0]}{last_name}"
        print(user_id)"""
        
        print(LDAP_CNUSER, LDAP_PASSWORD)
        #Init the database with postgres account
        database = Database(CONFIG["POSTGRES"]["host"],
            CONFIG["POSTGRES"]["database"],
            CONFIG["POSTGRES"]["user"],
            CONFIG["POSTGRES"]["password"])
            
        #Try to connect to databse
        if database.connect():
            print("Connected to the Database as Postgres")
            if uid:
                result = database.query(f"SELECT last_name, first_name, phone, type_user, access_token FROM USERS WHERE USERS.uid_user = '{uid}';")
                if result[0]:
                    values = result[1].fetchall()
                    user.last_name = values[0][0]
                    user.first_name = values[0][1]
                    user.phone = values[0][2]
                    user.type_u = values[0][3]
                    user.access_token = values[0][4]

                    if user.type_u == 0:
                        database.disconnect()

                        database = Database(CONFIG["POSTGRES"]["host"],
                            CONFIG["POSTGRES"]["database"],
                            "responsable",
                            "Responsable2025/")
                        
                        if database.connect():
                            print("Connected to the Database as Responsable")
                        else:
                            print("An error occured while connecting to the Database")
                            return False
                    else:
                        database.disconnect()

                        database = Database(CONFIG["POSTGRES"]["host"],
                            CONFIG["POSTGRES"]["database"],
                            "agent",
                            "Agent2025/")

                        if database.connect():
                            print("Connected to the Database as Agent")
                        else:
                            print("An error occured while connecting to the Database")
                            return False
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
    
    uuid4 = table.item(selected_item, 9).text()

    data = {"uuid":uuid4}
    print("uuid :", uuid4)
    result = requests.post(f"{API}delete_good", json=data, headers={'Authorization': f'Bearer {user.access_token}','Content-Type': 'application/json'})
    print(result.text)
    if result.status_code == 200:
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
    global loading
    loading = True
    table.setRowCount(0)

    users = get_user()

    if users == None or users == [] or len(users) == 0:
        return

    
    n_column = len(users[0]) 
    n_row = len(users)

    table.setRowCount(n_row)
    table.setColumnCount(n_column-2)

    i_row = -1
    i_column = -1

    for user in users:
        i_row += 1
        i_column = -1 
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

            if i_column == 4:
                break

    loading = False

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
    print(uuid4)
    print(selected_item)
    if(ldap_server.delete_user(table.item(selected_item, 4).text())):
        query = f"DELETE FROM USERS WHERE USERS.uid_user = '{uuid4}'; REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM {table.item(selected_item, 4).text()}; DROP USER {table.item(selected_item, 4).text()};"
        result = database.query(query)
        if result[0]:
            table.removeRow(selected_item)
            handle_message(success)
@private
def get_customer():
    if user.type_u == 0:
        query = "SELECT * FROM CLIENT;"
    else:
        query = f"SELECT * FROM CLIENT WHERE CLIENT.uid_user = '{user.uid}';"

    result  = database.query(query)
    
    if result[0]:
        values = result[1].fetchall()
        return values

@private
def set_customer(table, QTableWidgetItem):
    global loading
    loading = True
    table.setRowCount(0)

    customers = get_customer()

    if customers == None or customers == [] or len(customers) == 0:
        return

    print(customers)
    n_column = len(customers[0]) 
    n_row = len(customers)

    table.setRowCount(n_row)
    table.setColumnCount(n_column-1)

    i_row = -1
    i_column = -1

    for customer in customers:
        i_row += 1
        i_column = -1 
        for column in customer:
            if customer.index(column) == 0:
                print(column)
                table.setItem(i_row, 4, QTableWidgetItem(str(column)))
                continue

            i_column += 1

            table.setItem(i_row, i_column, QTableWidgetItem(str(column)))

            if i_column == 3:
                break

    loading = False

def customer_page(pages, table, QTableWidgetItem):
    pages.setCurrentIndex(8)
    set_customer(table, QTableWidgetItem)

@private
def get_owner():
    if user.type_u == 0:
        query = "SELECT * FROM CLIENT;"
    else:
        query = f"SELECT CLIENT.uid, CLIENT.nom, CLIENT.prenom, CLIENT.email, CLIENT.telephone FROM CLIENT WHERE CLIENT.uid_user = '{user.uid}';"

    result = database.query(query)
    print(result[1])
    if result[0]:
        values = result[1].fetchall()
        return values

@private
def set_proprio(table, QTableWidgetItem):
    global loading
    loading = True
    table.setRowCount(0)

    owners = get_owner()
    print(owners)
    if owners == None or owners == [] or len(owners) == 0:
        return

    print(owners)
    n_column = len(owners[0]) 
    n_row = len(owners)

    table.setRowCount(n_row)
    table.setColumnCount(n_column)

    i_row = -1
    i_column = -1

    for owner in owners:
        i_row += 1
        i_column = -1 
        for column in owner:
            if owner.index(column) == 0:
                table.setItem(i_row, 4, QTableWidgetItem(str(column)))
                continue

            i_column += 1

            table.setItem(i_row, i_column, QTableWidgetItem(str(column)))

    loading = False

def owner_page(pages, table, QTableWidgetItem):
    pages.setCurrentIndex(10)
    set_proprio(table, QTableWidgetItem)


def add_customer(last_name, first_name, email, phone, password, error, success):
    if last_name.text() == "" or first_name.text() == "" or phone.text() == "" or email.text() == "":
        handle_message(error)
        return False

    uuid4 = str(_generate_uuid4())

    data = {
            "uuid4":uuid4,
            "last_name":last_name.text(),
            "first_name":first_name.text(),
            "email":email.text(),
            "phone":phone.text(),
            "password":password.text(),
            "type":0,
        }

     
    result = requests.post(f"{API}add_user", json=data, headers={'Authorization': f'Bearer {user.access_token}','Content-Type': 'application/json'})
    print(result.text)

    if result.status_code == 200:
        query = f"INSERT INTO client VALUES ('{uuid4}', '{last_name.text()}', '{first_name.text()}', '{email.text()}', '{phone.text()}', '{user.uid}');"
        
        handle_message(success)
        last_name.setText("")
        first_name.setText("")
        email.setText("")
        phone.setText("")
        password.setText("")
        return database.query(query)[0]

def set_combo(combo):
    owners = get_owner()

    if owners == None or owners == [] or len(owners) == 0:
        return

    for owner in owners:
        combo.addItem(owner[1] + " " + owner[2], owner[0])

def add_good_page(pages, combo):
    pages.setCurrentIndex(2)
    set_combo(combo)

def delete_customer(table, success, error, QMessageBox):
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
    
    uuid4 = table.item(selected_item, 4).text()
    print("uuid :", uuid4)
    data = {"uuid":uuid4}
    
    result = requests.post(f"{API}delete_user", json=data, headers={'Authorization': f'Bearer {user.access_token}','Content-Type': 'application/json'})
    print(result.text)
    if result.status_code == 200:
        query = f"DELETE FROM CLIENT WHERE CLIENT.uid = '{uuid4}';"
        result = database.query(query)
        print(result[1])
        if result[0]:
            table.removeRow(selected_item)
            handle_message(success)

def delete_owner(table, success, error, QMessageBox):
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
    
    uuid4 = table.item(selected_item, 4).text()
    print(uuid4)
    query = f"DELETE FROM BIENS WHERE BIENS.uid_proprio = '{uuid4}'; DELETE FROM SUPERVISER WHERE SUPERVISER.uid_proprio = '{uuid4}'; DELETE FROM PROPRIETAIRE WHERE PROPRIETAIRE.uid_proprio = '{uuid4}';"
    result = database.query(query)
    print(result[1])
    if result[0]:
        table.removeRow(selected_item)
        handle_message(success)

def reload_table(table, QTableWidgetItem, type, row, QDate):
    #Reload Table
    if type == 0:
        set_goods(table, QTableWidgetItem)
    elif type == 1:
        set_customer(table, QTableWidgetItem)
    elif type == 2:
        set_proprio(table, QTableWidgetItem)
    elif type == 3:
        set_user(table, QTableWidgetItem)
    else:            
        set_events(table, QTableWidgetItem, QDate.fromString(table.item(row, 0).text(), "yyyy-MM-dd"))

def edit_row(row, column, table, type, QTableWidgetItem, success, error, QDate = None):
    if not loading:
        value = table.item(row, column).text()
        column_name_db = ["BIENS", "CLIENT", "PROPRIETAIRE", "USERS", "EVENT"]
        column_index = {0:{"id_bien":"str", "rue_bien":"str", "ville_bien":"str", "cpostal_bien":"int", "type_bien":"int", "surface_bien":"int", "nbr_piece_bien":"int", "prix":"int", "louable_achetable":"int", "uid_proprio":"str", "uid_user":"str"},
                        1:{"uid":"str", "nom":"str", "prenom":"str", "email":"str", "telephone":"str", "uid_user":"str"},
                        2:{"uid_proprio":"str", "nom":"str", "prenom":"str", "email":"str", "telephone":"str"},
                        3:{"uid_user":"str", "last_name":"str", "first_name":"str", "phone":"str", "type_user":"int", "login_id":"str"},
                        4:{"id_event":"str", "date_event":"str", "heure_event":"str", "libelle_event":"str", "rue_event":"str", "code_postal_event":"str", "ville_event":"str", "titre_event":"str", "uid_user":"str"}}
        uid_column = list(column_index[type].keys())[0]
        column_name = list(column_index[type].keys())[column+1]
        column_type = list(column_index[type].values())[column+1]
        
        print("Nom de la column : " + str(column_name), "Type de column : " + str(column_type), "Modified value : " + str(value))

        if column_name == "id_bien" or column_name == "uid_proprio" or column_name == "uid_user" or column_name == "uid" or column_name == "uid_proprio" or column_name == "type_user" or column_name == "login_id" or column_name == "id_event":
            print("Can't edit this column")
            handle_message(error)
            reload_table(table, QTableWidgetItem, type, row, QDate)
            return

        if type == 0:
            if column_name == "type_bien":
                if value == "Appartement":
                    value = 0
                elif value == "Maison":
                    value = 1
                elif value == "Terrain":
                    value = 2
                else:
                    return
            elif column_name == "louable_achetable":
                if value == "Location":
                    value = 0
                elif value == "Achetable":
                    value = 1
                else:
                    return
        
        if type in [0, 1]:
            data = {'column_name' : column_name, 'uuid': table.item(row, table.columnCount()-1).text(), 'value' : value, 'type' : type}

            result = requests.post(f"{API}edit", json=data, headers={'Authorization': f'Bearer {user.access_token}','Content-Type': 'application/json'})

            if result.status_code != 200:
                return

        if column_type == "int":
            query = f"UPDATE {column_name_db[type]} SET {column_name} = {value} WHERE {column_name_db[type]}.{uid_column} = '{table.item(row, table.columnCount()-1).text()}';"
        else:
            query = f"UPDATE {column_name_db[type]} SET {column_name} = '{value}' WHERE {column_name_db[type]}.{uid_column} = '{table.item(row, table.columnCount()-1).text()}';"

        print(query)
        result = database.query(query)
        if result[0]:
            print("Value as been edited !")
        else:
            print(result[1])

        handle_message(success)
        reload_table(table, QTableWidgetItem, type, row, QDate)

def get_stats(row, avg, month, total, table):
    uuid4 = table.item(row, table.columnCount()-1).text()
    print(uuid4)
    
    resultat = requests.post(f"{API}get_good_stats", json={"uuid":uuid4}, headers={'Authorization': f'Bearer {user.access_token}','Content-Type': 'application/json'})
    print("resultat : ", resultat.text)
    print('user : ', user.access_token)
    datas = json.loads(resultat.text)

    total_value = 0
    month_view = 0

    current_years = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    for data in datas['data']:
        total_value += data['view']

        date_split = data['date_s'].split('-')
        month_view += data['view'] if int(date_split[0]) == current_years and int(date_split[1]) == current_month else 0
    
    if(len(datas['data']) == 0):
        avg_value = 0
    else:
        avg_value = total_value / len(datas['data'])
    
    

    avg.setText(str(round(avg_value, 2)))
    month.setText(str(month_view))
    total.setText(str(total_value))