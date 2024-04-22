from entity import Admin, Person

import util
from authenticator import TextAuthenticator

admin_first_name = input("Enter Admin's First Name:\t")
admin_last_name = input("Enter Admin's Last Name:\t")
admin_national_id = input("Enter Admin's National ID:\t")
admin_password = input("Enter Admin's Password:\t")


admin = Admin(name=admin_first_name+" "+admin_last_name,nationalId=admin_national_id,password=admin_password)



