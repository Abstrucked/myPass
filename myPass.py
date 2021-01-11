import encryptor
import json
import pickle
from hashlib import sha256
import getch
import getpass
import os
# myPass custom imports
from myPass_utils.utils import clear, is_int
from credentials import Credentials as PassItem




# ----------------------------------------------------
# define Application UI-Header

def print_app_header(columns):
    print(columns*'_')
    print()
    print(f'{"- MANAGE YOUR PASSWORDS -":^{columns}}')
    print(columns*'_', '\n','\n')
# ----------------------------------------------------


# ----------------------------------------------------
# define Password List Class

class MyPass:
    """ Class definition of the Password_list """

    def __init__(self):
        """ Initialize the password_list as an empty array """
        self.__passwords = []
        self.terminal_columns = None
        self.terminal_rows = None

        try:
            self.e = encryptor.Encryptor()
            self.e.load_key()
            self.file_name =  sha256(self.e.key).hexdigest()            
        except ValueError:
            print('something went wrong')

    def get_terminal_size(self):
        self.terminal_columns, self.terminal_rows = os.get_terminal_size()
    
    
    def print(self, passwd_list):
        """ Returns a list of a string rappresentaiton of the passwords items """
        [passwd.print() for passwd in passwd_list]
        
    
    def add_password(self):
        """ Adds a password item to the passwords list and saves it to file""" 
        
        box_size = int(self.terminal_columns/2)
        
        print(f'{"*** ADD NEW CREDENTIALS":^{self.terminal_columns}}')
        print(f'{box_size*"-":^{self.terminal_columns}}')

        ref = input("Enter the reference:\t")
        usr_login = input('Enter the username:\t')
        passwd = getpass.getpass('Enter your password:\t')
        
        password = PassItem(ref, usr_login, self.e.encrypt_data(passwd.encode()))
        
        
        self.__passwords.append(password)
        self.save_to_file()

    
    def get_user_input(self):
        """ Returns the user input 
            - Main usage: menu choice
        """
        return input('enter your choice: ')

    
    def encrypt_data(self):
        pass

    
    def save_to_file(self):
        """ Saves an encrypted version of the current passwords list on file"""
        passwd_list = self.__passwords
        try:
            with open(self.file_name, 'wb') as f:
                data_to_save = {'password_list': passwd_list}
                encypted_data =self.e.encrypt_data(pickle.dumps(data_to_save))
                f.write(encypted_data)
            print('PASSWORDS have been saved to file')
            getch.getch()
        except IOError:
            print('IOERROR on saving thwe passwordlist')
    
    def load_from_file(self):
        """ 
            Loads and decrypts the saved passwords list from file
        """
        try:
            with open(self.file_name, 'rb') as f:
                try:
                    encrypted_data =self.e.decrypt_data(f.read())
                    data = pickle.loads(encrypted_data)
                    self.__passwords = data['password_list']
                except TypeError:
                    print('Couldnt decrypt the passwords file, check the validity of your key and the existence of the file')
                    print('1) If you like to generate a new key:')
                    print('q) To exit')
                    x = self.get_user_input()
                    if x == '1':
                        self.e.generate_key()
                        self.e.save_key()
                    elif x == 'q':
                        return
        except (IOError):
            print('something went wrong!')

    def menu(self):
        """ 
            Definition and implementation of UI 
        """
        in_menu = True
        while in_menu:
            clear()
            self.get_terminal_size()
            print_app_header(self.terminal_columns)
            print('- MENU -')
            print(self.terminal_columns*'-')
            print('(A)dd')
            print('(F)ind')
            print('(P)rint on screen')
            print('(S)ave')
            print('(L)oad')
            print('(Q)uit')
            print()
            choice = getch.getch()
            if choice == 'a' or choice == 'A':
                self.add_password()
            elif choice == 'f' or choice == 'F':
                self.find_passwords()
                
            elif choice == 'p' or choice == 'P':
                self.print(self.__passwords[:])
                getch.getch()
                clear()
            elif choice == 'l' or choice == 'L':
                self.load_from_file()
            elif choice == 'q' or choice == 'Q':
                print('quit')
                in_menu = False
            elif choice =='s' or choice =='S':
                self.save_to_file()
                getch.getch()
            else:
                print('enter a valid choice')


    def find_passwords(self):
        """ 
            Provides a UI and methods to search passwords 
        """
        clear()
        print_app_header(self.terminal_columns)
        # Search by reference
        print('*** PASSORD FINDER')
        print(self.terminal_columns*'_', '\n')
        ref = input('Search: (press ENTER to show all): ')        
        found = [passwd for passwd in self.__passwords[:] if ref in passwd.reference or ref in passwd.user_login]
        # MENU
        if len(found) < 1:
            print(self.terminal_columns*'-')
            print('*** Could not find any Credentials that match your search! (press anykey to continue)')
            getch.getch()
            return False
        sorted_list = []
        in_menu = True
        while in_menu:
            self.get_terminal_size()
            clear()
            print_app_header(self.terminal_columns)
            if len(sorted_list) > 0:
                print('here')
                found = sorted_list
            i = 0
            print(self.terminal_columns*'_','\n')
            print('*** ITEM SELECTION')
            print(self.terminal_columns*'_', '\n')
            print('{0:^4} {1:^30} {2:^20}'.format('Num', 'Reference', 'Username'))
            print('{0:4} {1:30} {2:20}'.format(4*'-', 30*'-', 20*'-'))

            for passwd in found:
                i = i + 1
                # print(i,')\t', passwd.reference, '\t', passwd.user_login)
                print('{0:3}) {1:30} {2:20}'.format(i, passwd.reference, passwd.user_login))
            print(self.terminal_columns*'-')
            print('r )\t sort by Reference')
            print('u )\t sort by Username')
            print('q )\t back to Main Menu')
            print(self.terminal_columns*'_','\n')
            choice= input('Select Credentials (Enter = 1): ')
            if choice== 'q':
                in_menu = False
            elif choice == 'r':
                sorted_list = sorted(found, key=lambda passwd: passwd.reference)
            elif choice == 'u':
                sorted_list = sorted(found, key=lambda passwd: passwd.user_login)    
            elif choice == 'i':
                sorted_list = sorted(found, key=lambda passwd: passwd.id)    
            elif choice == '':
                self.password_sub_menu('1', found)
            elif is_int(choice) and (int(choice) >= 0  and int(choice) <= len(found)):
               self.password_sub_menu(choice, found)
            else:
                pass
   
   
    def password_sub_menu(self, choice, password_list):
        """ 
            Single credentials manager menu.
        """
        while True:
            self.get_terminal_size()
            clear()
            print_app_header(self.terminal_columns)
            passwd_list = self.__passwords[:]
            selected = password_list[int(choice)-1]
            selected.print()
            print(10*'-', 'Manage Credentials', 10*'-','\n')
            print('1)\t Show Password')
            print('2)\t Edit Reference')
            print('3)\t Edit Username')
            print('4)\t Change Password')
            print('5)\t Delete Credentials')
            print(self.terminal_columns*'-')
            print('s)\t Save Changes')
            print('q)\t to Search Result')
            print()
            submenu_choice = input('Enter your choice: ')
            if submenu_choice == '1':
                print(self.terminal_columns*'_', '\n')
                decoded_password = self.e.decrypt_data(selected.password).decode()
                print('Username:\t\t', selected.user_login)
                print('Password:\t\t', decoded_password)
                getch.getch()
                clear()   
            elif submenu_choice == '2':
                new_reference = input('Enter new reference name: ')
                for passwd in passwd_list:
                    if passwd.id == selected.id:
                        passwd.reference = new_reference
                clear()
            elif submenu_choice == '3':
                new_username = input('Enter new username: ')
                for passwd in passwd_list:
                    if passwd.id == selected.id:
                        passwd.user_login = new_username
                clear()
            elif submenu_choice == '4':
                new_password = input('Enter new password: ')
                for passwd in passwd_list:
                    if passwd.id == selected.id:
                        passwd.password =  self.e.encrypt_data(new_password.encode())
                clear()
            elif submenu_choice == '5':
                password_list.remove(selected)
                self.__passwords.remove(selected)
                print('Credentials removed.')
                self.save_to_file()
                getch.getch()
                return False
            elif submenu_choice =='s':
                self.save_to_file()
                
            elif submenu_choice == 'q':
                return False
    
    

# ----------------------------------------------------
# Application Runner
# ----------------------------------------------------

if __name__ == "__main__":
    app = MyPass()
    app.load_from_file()
    clear()
    app.menu()
    clear()
#  ---------------------------------------------------
