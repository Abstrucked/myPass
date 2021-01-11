from cryptography.fernet import Fernet, InvalidToken
import cryptography.exceptions as CryptoErrors

class Encryptor:
    def generate_key(self):
        self.key = Fernet.generate_key()    

    def save_key(self):
        with open('mykey.key', 'wb') as fw:
            fw.write(self.key)
        print('Key saved')

    def load_key(self):
        try:
            with open('mykey.key', 'rb') as fr:
                self.key = fr.read()
        except IOError:
            print('File Not Found')
        

    def encrypt_file(self, original_data: bytes, encrypted_file: str):
        
        fernet = Fernet(self.key)
        
        encrypted_data = fernet.encrypt(original_data)

        with open(encrypted_file, 'wb') as fw:
            fw.write(encrypted_data)

    def encrypt_data(self, data: bytes):
        try:
            fernet = Fernet(self.key)
            enc_data = fernet.encrypt(data)
            return enc_data
        except ValueError:
            print('Key not valid!')

    def decrypt_file(self, encripted_file):
        fernet = Fernet(self.key)
        with open(encripted_file, 'rb') as fr:
            data = fr.read()
        decrypted_data = fernet.decrypt(data)
        return decrypted_data

    def decrypt_data(self, data: bytes):
        try:
            fernet = Fernet(self.key)
            return fernet.decrypt(data)
        except (InvalidToken, ValueError):
            print('Key Token not Valid')