from abc import ABC, abstractmethod
from authenticator import TextAuthenticator
from loguru import logger
import util
#TODO: add details
#TODO: add propper error handeling 
class Entity(ABC):
    pass
    # @abstractmethod
    # def show_details():
    #     ...
        

class Person(Entity):
    def __init__(self,name:str,nationalId:str) -> None:
        super().__init__()
        
        while not Person.check_natioanl_id(nationalId):
            print(f"""National Id ({nationalId}) is not formatted properly.\n
                   It should contain only numbers and be 10-digits long.""")
    
            nationalId = input("Enter Admin's National ID:\t")
    


    def check_natioanl_id(nationalId:str) -> bool:
        # check if national ID is formatted correctly
        return len(nationalId) == 10 and str.isnumeric(nationalId)

        
class Admin(Person):
    def __init__(self, name: str, nationalId: str,password:str) -> None:
        super().__init__(name, nationalId)
        
        self.auth = TextAuthenticator()
        while not self.auth.check_password(password):
            print("The supplied Passowrd is wrong.")
            password = input("Enter Admin's Password:\t")
            
        self.bankIdPool = util.get_random_id_pool(4)
        
    
        
    def change_password(old_password:str,new_password:str):
        