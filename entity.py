from abc import ABC, abstractmethod
from authenticator import TextAuthenticator
from loguru import logger
import util


#TODO: add details
#TODO: add propper error handeling 


class Person(ABC):
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
    def __init__(self, name: str, nationalId: str,password:str,store) -> None:
        super().__init__(name, nationalId)
        
        self.auth = TextAuthenticator()
        while not self.auth.check_password(password):
            print("The supplied Passowrd is wrong.")
            password = input("Enter Admin's Password:\t")
            
        self.bankIdPool = store.bankIdPool
        self.password = password
        
        self.banks = store.banks
        
    
        
    def change_password(self,new_password:str):
        if self.auth.change_password(self.password,new_password):
            print(f"Password was successfully changed to {new_password}.")
        else:
            print("There was a problem with changing your password.")
            
    def create_a_bank(self,name:str):
        
        if self.bankIdPool == []:
            print("There is no ID left to assign to a new bank.")
            return None
        else:
            newBankId = self.bankIdPool.pop()
            newBank = Bank(name=name,bankId=newBankId)
            self.banks[newBankId] = newBank
            print(f"A new bank with the name {name} and {newBankId} ID number was created.")
            return newBank
        
    def create_a_branch(self,name:str,bankId:str,budget:int):
        bank = self.banks.get(bankId)
        if bank == None:
            print("The specified bank does not exist.\nYou must first create the bank.")
            return None
        else:
            if bank.branchPoolId == []:
                print("There is no ID left to assign to a new branch.")
                return None
            else:
                newBranchId = bank.branchIdPool.pop()
                newBranch = Branch(name=name,bankId=bankId,branchId=newBranchId,budget=budget)
                bank.branches[newBranchId] = newBranch
                print(f"A new branch with the ID of {newBranchId} was added to bank of {bank.name}.")
                return newBranch
            
            
    def adjust_budget(self,bankId:str,branchId:str,transaction_amount:int):
        branch = self.banks.get(bankId).branches.get(branchId)
        branch.budget += transaction_amount
        print(f"The budget of branch {branch.name} of the {self.banks.get(bankId).name} bank was adjusted to {branch.budget}.")
        
    
    def remove_bank(self,bankId:str):
        bank = self.banks.get(bankId)
        print("You are deleting the following bank from the system.")
        bank.show_details()
        answer = input("Are you sure?(y/n)")
        if answer[0] == 'y' or answer[1] == 'Y':
            self.banks.pop(bankId)
            print("Bank deleted successfully.")
            
        else:
            print("Deletion cancelled.")
            
    def remove_branch(self,bankId:str,branchId:str):
        bank = self.banks.get(bankId)
        branch = bank.branches.get(branchId) 
        print("You are deleting the following branch from the system.")
        branch.show_details()
        answer = input("Are you sure?(y/n)")
        if answer[0] == 'y' or answer[1] == 'Y':
            self.banks.get(bankId).branches.pop(branchId)
            print("Branch deleted successfully.")
            
        else:
            print("Deletion cancelled.")
            
            
    
        
class Account():
    def __init__(self,accountId:str,ammount:int,nationalId:str) -> None:
        self.accountId = accountId
        self.ammount = ammount
        self.owner = nationalId
    
    def show_details(self):
        print("\tAccount Details")
        print(f"\tNational ID: {self.owner}")
        print(f"\tAmmount: {self.ammount}")
        print(f"\tAccount ID: {self.accountId}")
        
        
class Customer(Person):
    def __init__(self, name: str, nationalId: str,address:str,store) -> None:
        super().__init__(name, nationalId)
        self.address = address
        self.accounts = {}
        self.loans = []
        self.store = store
        
    def create_account(self,bankId,branchId):
        branch = self.store.banks.get(bankId).branches.get(branchId)
        accountSubId = branch.accountIdPool.pop()
        accountId = bankId + branchId + accountSubId
        account = Account(accountId=accountId,ammount=0,nationalId=self.nationalId)
        self.accounts.append(account)
        branch.accounts[accountId] = account
        print(f"Account Created with ID: {accountId}")
        account.show_details()

    def take_loan(self,ammount,accountId):
        branchId = accountId[2:4]
        bankId = accountId[0:2]
        
        if branchId in [account[2:4] for account in self.accounts] and branchId not in self.loans:
            if self.store.banks.get(bankId).branches.get(branchId).budget > ammount:
                self.store.banks.get(bankId).branches.get(branchId).budget -= ammount
                self.store.banks.get(bankId).branches.get(branchId).accounts.get(accountId[4:8]).ammount += ammount
                self.loans.append(branchId)
        else:
            print("You dont have an account in the specifed branch")
    
    
    def deposit(self,accountId:str,ammount: int):
        if accountId not in self.accounts.keys:
            print("You dont have such an account.")
            
        else:
            account = self.accounts[accountId]
            account.ammount += ammount
            print(f"Deposit to {accountId} owned by {account.owner} made.\nNew balance is: {account.ammount}")
    
    def withdraw(self,accountId:str,ammount: int):
        if accountId not in self.accounts.keys:
            print("You dont have such an account.")
            
        else:
            account = self.accounts[accountId]
            if account.ammount < ammount:
                print("Inusfficent funds.")
            else:
                account.ammount -= ammount
                print(f"Withdraw from {accountId} owned by {account.owner} made.\nNew balance is: {account.ammount}")
                
    def show_details(self):
        print("\tCustomer Details")
        print(f"\tName: {self.name}")
        print(f"\tNational ID: {self.nationalId}")
        print(f"\tAddress: {self.address}")
        print(f"\tAccounts: {self.accounts}")
        

class Entity(ABC):
    name:str
    
    @abstractmethod
    def show_details():
        pass
        

class Bank(Entity):
    def __init__(self,name:str,bankId:str) -> None:
        self.name = name
        self.bankId = bankId
        self.branchPoolId = util.get_random_id_pool(2)
        self.branches = {}
        
    def show_details(self):
        print("\tBank Details")
        print(f"\tName: {self.name}")
        print(f"\tBank ID: {self.bankId}")
        print(f"\tBranch Count: {len(self.branches)}")
        
    
class Branch(Entity):
    
    def __init__(self,name:str,bankId:str,branchId:str,budget:int) -> None:
        super().__init__()
        self.name = name
        self.bankId = bankId
        self.branchId = branchId
        self.accountIdPool = util.get_random_id_pool(4)
        self.accounts = {}
        
        
    def show_details(self):
        print("\tBranch Details")
        print(f"\tName: {self.name}")
        print(f"\tBank ID: {self.bankId}")
        print(f"\tBranch ID: {self.branchId}")
        print(f"\tAccount Count: {len(self.accounts)}")
        
 
        
        
        
