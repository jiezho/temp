from flask_script import Manager

DBmanager = Manager() # 这个为什么不是Manager(app)。因为这个不是主文件，所以不需要在Manager()里面写入'app'

@DBmanager.command
def init():
    print('数据库初始化完成')

@DBmanager.command
def migrate():
    print('数据表重新迁移成功')

# 这个没有下面的代码是因为这个不是主的manager.py。它只是子的文件，所以不需要有下面的代码。
'''
if __name__ == '__main__':
    manager.run()
'''