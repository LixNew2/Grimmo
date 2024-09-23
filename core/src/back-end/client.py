import configparser
from classes.LDAPServer import LDAPServer

LDAP_CONFIG = configparser.ConfigParser()
LDAP_CONFIG.read("core\config\config.cfg")


LDAP_CNUSER = input("CN : ")
LDAP_PASSWORD = input("Password : ")

ldap_server = LDAPServer(LDAP_CONFIG["LDAP"]["ldap_url"],
                         int(LDAP_CONFIG["LDAP"]["ldap_port"]),
                         LDAP_CONFIG["LDAP"]["ldap_base"])

ldap_server.login(LDAP_CNUSER, LDAP_PASSWORD) #ok

#Error during add methode user
cn = input("Nom complet : ")
sn = input("Nom de famille : ")
sAMAccountName = cn[0].lower() + sn.lower()
userPrincipalName = sAMAccountName + LDAP_CONFIG["LDAP"]["DOMAIN"]
phone_number = input("phone_number : ")
mail = input("mail : ")
password = input("password : ")
gp_name = input("gp_name : ")

print(ldap_server.add(cn, sn, sAMAccountName, userPrincipalName, phone_number, mail, password, gp_name))