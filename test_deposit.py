from entity import Admin, Person
from entity import Customer 
from store import store

def test_deposit():
    
    storage = store()

    admin_first_name = "jack"
    admin_last_name = "kasd"
    admin_national_id = "1231231320"
    admin_password = "Banker1939"

    admin = Admin(name=admin_first_name+" "+admin_last_name,nationalId=admin_national_id,password=admin_password,store=storage)
    a = admin.create_a_bank("jamesTown")
    ab = admin.create_a_branch("ny",a.bankId,500000)

    james = Customer("james","1231231389","ny",storage)

    acc1 = james.create_account(ab.bankId,ab.branchId)

    acc2 = james.create_account(ab.bankId,ab.branchId)


    james.deposit(acc1.accountId,50020)

    
    assert acc1.ammount == 50020
