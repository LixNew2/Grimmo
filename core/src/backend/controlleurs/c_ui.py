

from core.src.backend.classes.models.LDAPServer import LDAPServer
from core.src.backend.classes.models.Database import Database
from core.src.backend.config.config import CONFIG
from PrivateCode import private
from core.src.backend.classes.User import User

import uuid
from uuid import UUID

ldap_server : LDAPServer
database : Database
user : User

@private
def _generate_uuid4() -> UUID:
    return uuid.uuid4()

def login(LDAP_CNUSER, LDAP_PASSWORD, pages) -> bool:
    #Init the LDAP server
    global ldap_server, user, database

    ldap_server = LDAPServer(CONFIG["LDAP"]["ldap_url"],
                    int(CONFIG["LDAP"]["ldap_port"]),
                    CONFIG["LDAP"]["ldap_domain"],
                    CONFIG["LDAP"]["ldap_base"])

    #Try to login
    if ldap_server.login(LDAP_CNUSER, LDAP_PASSWORD):
        #Check if the user is in the group "Responsable"
        print("Connected with LDAP")
        
        #Get user data
        groups = ldap_server.get_groups(LDAP_CNUSER)
        uid = ldap_server.get_uid(LDAP_CNUSER)
        if uid:
            result = database.query(f"""
                                        SELECT nom_agent, prenom_agent, tel_agent FROM USERS
                                        WHERE users.uid = '{uid}';
                                        """)
            if result[0]:
                values = result[1].fetchall()

        user = User(LDAP_CNUSER, groups, uid, values[0][0], values[0][1], values[0][2])

        #Init the database
        database = Database(CONFIG["POSTGRES"]["host"],
            CONFIG["POSTGRES"]["database"],
            #
            CONFIG["POSTGRES"]["user"],
            CONFIG["POSTGRES"]["password"])
            
        #Try to connect to databse
        if database.connect():
            print("Connected to the Database")
            #Display success
            """display success"""

    else:
        #Display error
        """display error"""
        return False
    
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
def _add_user_to_db(uuid4, last_name, first_name, phone) -> bool :
    query = f"INSERT INTO users VALUES ({uuid4}, {last_name}, {first_name}, {phone})"
    return database.query(query)[0]

def add_user(last_name, first_name, password, phone, gp_name) -> bool :
    if "Responsable" in user.groups:
        uuid4 = str(_generate_uuid4())
        if _add_user_to_ad(last_name, first_name, password, gp_name, uuid4):
            if _add_user_to_db(uuid4, last_name, first_name, phone):
                return True
    return False