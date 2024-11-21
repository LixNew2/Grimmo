from ldap3 import Server, Connection, ALL, MODIFY_ADD, MODIFY_REPLACE
import time
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
    def __init__(self, ldap_url : str, ldap_port : int, ldap_domain : str, search_base: str) -> None:
        self.BASE = search_base;
        self.server = Server(ldap_url, ldap_port, get_info=ALL)
        self.CONN = None
        self.DOMAIN = ldap_domain

    def __str__(self) -> str:
        return f"LDAP Server at {self.BASE}"

    #Methodes
    def login(self, ldap_login : str, ldap_password : str):
        try:
            #Instanciate the connection
            self.CONN = Connection(self.server, ldap_login, ldap_password, auto_bind=True)
            return True
            
        except Exception as e:
            print(e)
            print("Error while connecting to the LDAP server")
            return False
    
    """def change_password(self, cn_user, pdw) -> bool:
        user_dn = f"CN={cn_user},OU=Users,OU=Grimmo,{self.BASE}"
        if self.conn.extend.microsoft.modify_password(user_dn, pdw):
            return [True]
        return [False, self.CONN.result['description']]"""

    """def get_pdw_last_set(self, cn_user : str) -> str:
        try:
            # Get the attribut uid of the user
            if self.CONN.search(self.BASE, f'(CN={cn_user})', attributes=['pwdLastSet']):
                # Check if the user have uid attribute
                if len(self.CONN.entries) > 0 and hasattr(self.CONN.entries[0], 'pwdLastSet'):
                    # Return the uid
                    return self.CONN.entries[0].uid.value
                else:
                    return None
            else:
                return None
        except Exception as e:
            print(e)
            return None"""
        
    def get_groups(self, cn_user : str) -> list:
        #Get Distinguished Name of the user
        if self.CONN.search(self.BASE, f'(CN={cn_user})', attributes=['distinguishedName']):
            user_dn = self.CONN.entries[0].distinguishedName
            
            #Group search filter
            group_search_filter = f'(&(objectClass=group)(member={user_dn}))'
            
            #Search for the group
            try:
                self.CONN.search(self.BASE, group_search_filter, attributes=['cn'])
                #Return list of user groups
                return [group.cn for group in self.CONN.entries]
            except:
                return print("An Error occured while searching for groups")
            
    def get_uid(self, cn_user : str) -> str:
        try:
            # Get the attribut uid of the user
            if self.CONN.search(self.BASE, f'(CN={cn_user})', attributes=['uid']):
                # Check if the user have uid attribute
                if len(self.CONN.entries) > 0 and hasattr(self.CONN.entries[0], 'uid'):
                    # Return the uid
                    return self.CONN.entries[0].uid.value
                else:
                    return None
            else:
                return None
        except Exception as e:
            print(e)
            return None

    
    def add_user(self, last_name, first_name, password, gp_name, uuid4) -> bool:
        try:
            full_name = f"{last_name.upper()} {first_name.upper()}"
            user_id = f"{first_name[0].upper()}{last_name[0].upper()}{last_name[1:].lower()}"

            print(password)
            # Attributes of new user
            user_attributes = {
                'objectClass': ['person', 'top', 'organizationalPerson', 'user'],
                'cn': full_name,
                'sn': last_name,
                'givenName': first_name,
                'userPassword': str(password),
                'sAMAccountName': user_id,
                'userPrincipalName': f"{user_id}{self.DOMAIN}",
                'displayName': full_name,
                'uid' : str(uuid4),
                'pwdLastSet' : -1,
                'userAccountControl' : 544
            }

            # User DN
            user_dn = f"CN={full_name},OU=Users,OU=Grimmo,{self.BASE}"
            # Add user to AD
            self.CONN.add(user_dn, attributes=user_attributes)

            if self.CONN.result['result'] == 0:
                print("User added to AD")

                # Groupe DN
                group_dn = f"CN={gp_name},OU=Groups,OU=Grimmo,{self.BASE}"
                # Add user to group
                self.CONN.modify(group_dn, {'member' : [(MODIFY_ADD, [user_dn])]})

                if self.CONN.result['result'] == 0:
                    print("User added to group")
                else:
                    print(self.CONN.result['description'])
                    return False

                # Active account
                """self.CONN.modify(user_dn, {'userAccountControl': [(MODIFY_REPLACE, [512])]})
                if self.CONN.result['result'] == 0:
                    print("ok")
                else:
                    print(self.CONN.result['description'])"""

                return True
            else:
                print(self.CONN.result['description'])
                return False
            
        except Exception as e:
            print(e)
            return False
        
    def disconnect(self) -> None:
        try:
            self.CONN.unbind()
        except:
            print("An error occured while disconnecting from the LDAP server")
        print("Disconnected from the LDAP server")

    def delete_user(self, cn_user : str) -> bool:
        print(cn_user)
        try:
            if self.CONN.search(self.BASE, f'(CN={cn_user})', attributes=['distinguishedName']):
                user_dn = self.CONN.entries[0].distinguishedName.value

                self.CONN.delete(user_dn)
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False