from ldap3 import Server, Connection, ALL

class LDAPServer:
    """
    This class is used to interact with an LDAP server
    
    Args:
        - ldap_url : str : The URL of the LDAP server | Example: "ldap://127.0.0.1:389"
        - ldap_port : int : The port of the LDAP server | Example: 389
        - ldap_login : str : CN of the user | Example: "Admin
        - ldap_password : str : The password of the user | Example: "password"
        - search_base : str : The search base of the LDAP server | Example: "DC=example,DC=com"

    Returns:
        - None
    """
    #instance Methodes

    def __init__(self, ldap_url : str, ldap_port : int, search_base: str) -> None:
        self.BASE = search_base;
        self.server = Server(ldap_url, ldap_port, get_info=ALL)
        self.CONN = None

    def __str__(self) -> str:
        return f"LDAP Server at {self.BASE}"

    #Methodes
    def login(self, ldap_login : str, ldap_password : str):
        try:
            self.CONN = Connection(self.server, ldap_login, ldap_password, auto_bind=True)
            print("Connected !")
        except:
            print("Error while connecting to the LDAP server")

    def check_groups(self, search_filter : str, group : str) -> None:
        #Get Distinguished Name of the user
        if self.CONN.search(self.BASE, f'(CN={search_filter})', attributes=['distinguishedName']):
            user_dn = self.CONN.entries[0].distinguishedName
            
            #Group search filter
            group_search_filter = f'(&(objectClass=group)(member={user_dn}))'
            
            #Search for the group
            try:
                self.CONN.search(self.BASE, group_search_filter, attributes=['cn'])
                #Check if the user is in the group and return True if he is
                for entry in self.CONN.entries:
                   if entry.cn == group:
                        return True
                return False
            except:
                return print("An Error occured while searching for groups")
    
    def add(self, cn, sn, sAMAccountName, userPrincipalName, phone_number, mail, password, gp_name) -> bool:
        user_attributes = {
            'objectClass': ['inetOrgPerson', 'organizationalPerson', 'person', 'top'],
            'cn': cn,
            'sn': sn,
            'sAMAccountName': sAMAccountName,
            'userPrincipalName': userPrincipalName,
            'telephoneNumber': phone_number,
            'mail': mail,
            'userPassword': password
        }

        user_dn = f"CN={cn} {sn},OU=Grimmo,OU=User,DC=gli,DC=local"
        group_dn = f"CN={gp_name},OU=Grimmo,OU=User,DC=gli,DC=local"


        self.CONN.add(user_dn, attributes=user_attributes)
        self.CONN.modify(user_dn, {'member': [('MODIFY_ADD', group_dn)]})

        if self.CONN.result['result'] == 0:
            return True
        else:
            print(self.CONN.result['description'])
            return False

    def set_group(self, cn : str, gp_name : str) -> bool : ...


