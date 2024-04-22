
import os
import hashlib
from abc import ABC,abstractmethod
import bcrypt


class Authenticator(ABC):
    @abstractmethod
    def check_password(candidate_password: str) -> bool:
        ...

    @abstractmethod
    def change_password(old_password: str, new_password: str) -> bool:
        ...


class TextAuthenticator(Authenticator):
    def __init__(self):
        default = 'Banker1939'
        hashed = self.hasher(default)
        self.password_path = 'password.txt'
        if not os.path.exists(self.password_path):
            self.save_hash(self.password_path,hashed)
     

    def hasher(self,password: str):

        # Generate salt
        mySalt = bcrypt.gensalt()

        # Hash password
        return bcrypt.hashpw(password.encode('utf-8'), mySalt)

    def read_hash(self,file_path: str):
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                hashed_password = file.read()
                return hashed_password
        else:
            print("Password file does not exist.")
    def save_hash(self,file_path, hashed_password):
    
        with open(file_path, 'wb') as file:
            file.write(hashed_password)

      

    def check_password(self, password: str):
        return bcrypt.checkpw(password.encode('utf-8'), self.read_hash(self.password_path))

    def change_password(self,old_password: str, new_password: str):
        if self.check_password(old_password):
            if os.path.exists(self.password_path):
                try:
                    os.remove(self.password_path)
                
                except Exception as e:
                    print(f"Error deleting passwordfile: {e}")
            
            
            # save new pass
            self.save_hash(self.password_path,self.hasher(new_password)) 
            return True   
        else:
            return False