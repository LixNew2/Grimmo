

from core.src.backend.classes.models.LDAPServer import LDAPServer
from core.src.backend.classes.models.Database import Database
from core.src.backend.config.config import CONFIG
from PrivateCode import private
from core.src.backend.classes.User import User

ldap_server = None
database = None
user = None

def login(LDAP_CNUSER, LDAP_PASSWORD, pages):
    #Init the LDAP server
    global ldap_server, user, database

    ldap_server = LDAPServer(CONFIG["LDAP"]["ldap_url"],
                    int(CONFIG["LDAP"]["ldap_port"]),
                    CONFIG["LDAP"]["ldap_base"])

    #Try to login
    if ldap_server.login(LDAP_CNUSER, LDAP_PASSWORD):
        #Check if the user is in the group "Responsable"
        print("Connected with LDAP")
    
        groups = ldap_server.get_groups(LDAP_CNUSER)
        user = User(LDAP_CNUSER, groups)

        #Init the database
        database = Database(CONFIG["POSTGRES"]["host"],
            CONFIG["POSTGRES"]["database"],
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
        return
    
    pages.setCurrentIndex(1)

@private
def _check_user_groups(search) -> bool:
    for group in user.groups:
        if group == search:
            return True
    return False

@private
def _add_user_to_ad():
    cn = input("Prenom : ")
    sn = input("Nom de famille : ")
    sAMAccountName = cn[0].lower() + sn.lower()
    userPrincipalName = sAMAccountName + CONFIG["LDAP"]["DOMAIN"]
    phone_number = input("phone_number : ")
    mail = input("mail : ")
    password = input("password : ")
    gp_name = input("gp_name : ")

    ldap_server.add(cn, sn, sAMAccountName, userPrincipalName, phone_number, mail, password, gp_name)

@private
def _add_user_to_db(last_name, first_name, phone_number, email, password, groups, street, city, pcode) -> None :
    QUERY = f"INSERT INTO users VALUES ({first_name[0].upper() + last_name.lower()}, {last_name}, {first_name}, {phone_number}, {email}, {password}, {groups}, {street}, {city}, {pcode})"
    database.query(QUERY)

def add_user(last_name, first_name, phone_number, email, password, groups, city, codep, street) -> None :
    if "Responsable" in user.groups:
        _add_user_to_ad(last_name, first_name, phone_number, email, password, groups, city, codep, street)
        _add_user_to_db(last_name, first_name, phone_number, email, password, groups, city, codep, street)

