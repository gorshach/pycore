from mysql import Mysql

user = Mysql('test')
#ret = user.where(id=100).where(name='fwe').delete()
#print(ret)
user.save(name='guobin1')
print(user.save(name='guobin2'))
user.name = 'guobin8'
print(user.save())