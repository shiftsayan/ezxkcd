import os
import getpass

ID = input('\nFacebook Numeric ID: ')
Password = getpass.getpass('Password: ')
os.environ['ID'] = str(ID)
os.environ['PASSWORD'] = str(Password)
