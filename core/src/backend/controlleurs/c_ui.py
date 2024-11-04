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

@private
def _generate_uuid4() -> UUID:
    return uuid.uuid4()

def login(LDAP_CNUSER, LDAP_PASSWORD, pages, username, menu) -> bool:
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
                result = database.query(f"SELECT nom_user, prenom_user, tel_user, type_user FROM Users WHERE Users.uid_user = '{uid}';")
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
    pages.setCurrentIndex(1)
    return True

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
    query = f"INSERT INTO Users VALUES ('{uuid4}', '{last_name}', '{first_name}', '{phone}', '{type}');"
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
    global ldap_server, database
    ldap_server.disconnect()
    database.disconnect()
    menu.hide()
    pages.setCurrentIndex(0)
    ldap_server = None
    database = None