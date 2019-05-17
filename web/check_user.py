from database.database import *

users = select_users()

print('id\t\t|password\t\t|guid')
for u in users:
	print(u.id + '\t\t|' + u.password + '\t\t|'+ u.guid)


