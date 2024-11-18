from core.src.backend.classes.models.LDAPServer import LDAPServer
from core.src.backend.classes.models.Database import Database
from core.src.backend.config.config import CONFIG
from PrivateCode import private
from core.src.backend.classes.User import User

import uuid
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
def _add_user_to_db(uuid4, last_name, first_name, phone, type) -> bool :
    query = f"INSERT INTO USERS VALUES ('{uuid4}', '{last_name}', '{first_name}', '{phone}', '{type}');"
    return database.query(query)[0]

def add_user(last_name, first_name, password, phone, gp_name) -> bool :
    print(user.type_u)
    if user.type_u == 0:
        print("User in creation")
        uuid4 = str(_generate_uuid4())
        if _add_user_to_ad(last_name, first_name, password, gp_name, uuid4):
            if _add_user_to_db(uuid4, last_name, first_name, phone, 0 if gp_name == "Responsable" else 1):
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

def add_good(city, address, cp, type_good, surface, nbr_room, commendable_purshasable, price) -> bool:
    """
    If buy is checked commendable_purshasable = 1
    If rent is checked commendable_purshasable = 0
    """
    global user

    if type_good == "Appartement":
        type_good = 0
    elif type_good == "Maison":
        type_good = 1
    else:
        type_good = 2 #Terrain

    uuid4 = str(_generate_uuid4())
    query = f"INSERT INTO BIENS VALUES ('{uuid4}', '{address}', '{city}', '{cp}', {type_good}, {surface}, {nbr_room}, {price}, {commendable_purshasable}, '{user.uid}');"
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


def add_event(date, hours, desc, street, cp, city, title): 
    if (date == None or hours == None or desc == "" or street == "" or cp == "" or city == "" or title == ""):
        return False
    
    uuid4 = str(_generate_uuid4())
    query = f"INSERT INTO EVENT VALUES ('{uuid4}', '{date.toString('dd/MM/yyyy')}', '{hours.toString('HH:mm')}', '{desc}', '{street}', {cp}, '{city}', '{title}', '{user.uid}');"
    print(database.query(query)[1])

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
            query = f"SELECT * FROM EVENT WHERE EVENT.date_event = '{selected_date}' AND EVENT.uid_user = {user.uid};"
        
        result = database.query(query)
        
        if result[0]:
            return result[1].fetchall()

def set_events(table, QTableWidgetItem, date = None) -> None:
    table.setRowCount(0)

    if date == None:
        events = get_events()
    else:
        events = get_events(date)

    if events == None:
        return
    
    if len(events) == 0:
        return
    
    n_column = len(events[0]) 
    n_row = len(events)

    table.setRowCount(n_row)
    table.setColumnCount(n_column-2)

    i_row = -1
    i_column = -1

    for event in events:
        i_row += 1
        i_column = -1 
        print(event)
        for column in event:
            if event.index(column) == 0: #skip the id
                continue

            i_column += 1

            table.setItem(i_row, i_column, QTableWidgetItem(str(column)))

def home_page(pages, table1, table2, QTableWidgetItem, add_user_home):
    if user.type_u == 1: 
        add_user_home.hide()

    pages.setCurrentIndex(1)
    set_goods(table1, QTableWidgetItem)
    set_events(table2, QTableWidgetItem)

def goods_page(pages, table, QTableWidgetItem):
    pages.setCurrentIndex(4)
    set_goods(table, QTableWidgetItem)

def set_goods(table, QTableWidgetItem):
    goods = get_goods()

    if goods == None:
        return

    n_column = len(goods[0]) 
    n_row = len(goods)

    table.setRowCount(n_row)
    table.setColumnCount(n_column-2)

    i_row = -1
    i_column = -1

    for good in goods:
        i_row += 1
        i_column = -1
        for column in good:
            if good.index(column) == 0: #skip the id
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
        
def login(LDAP_CNUSER, LDAP_PASSWORD, pages, username, menu, table1, table2, QTableWidgetItem, add_user_home) -> bool:
    #Init the LDAP server
    global ldap_server, user, database

    #Try to login
    if ldap_server.login(LDAP_CNUSER, LDAP_PASSWORD):     
        #Get user data
        groups = ldap_server.get_groups(LDAP_CNUSER)
        uid = ldap_server.get_uid(LDAP_CNUSER)
        
        user = User(LDAP_CNUSER, groups, uid, None, None, None, 1)

        #Init the database
        database = Database(CONFIG["POSTGRES"]["host"],
            CONFIG["POSTGRES"]["database"],
            #
            CONFIG["POSTGRES"]["user"],
            CONFIG["POSTGRES"]["password"])
            
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
        #Display error
        """display error"""
        return False
    
    menu.show()
    username.setText(LDAP_CNUSER)
    home_page(pages, table1, table2, QTableWidgetItem, add_user_home)
    print("UID : ", user.uid)
    print("Groups : ", str(user.groups))
    print("CN : ", user.cn)
    print("Last Name : ", user.last_name)
    print("First Name : ", user.first_name)
    print("Phone : ", user.phone)
    print("Type : ", str(user.type_u))
    return True