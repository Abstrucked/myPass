from hashlib import sha256

# ----------------------------------------------------
# define Single Credentials Class


class Credentials:
    """Class definition of a Password Item"""
    def __init__(self, ref, usr_login, passwd):
        """ Constructor of a Password Item 

            Arguments:

            -reference: Reference to the service to login

            -usr_login: Login credentials for the reference service

            -password:  Password for the service
        """
        
        self.reference = ref
        self.user_login = usr_login
        self.password = passwd
        self.id = sha256((ref + usr_login).encode()).hexdigest()


    def print(self):
        print(40*'-')
        print('Reference:\t', self.reference)
        print('Username:\t', self.user_login)
        print('Password:\t', 8*'*')


    def to_string(self):
        """ Returns a string of an OrderDict rapresentation of the password item """
        return str(self.__dict__)


