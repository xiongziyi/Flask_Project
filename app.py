from flask import Flask,render_template
from View import  *
from flask_sqlalchemy import SQLAlchemy
from werkzeug import  security
from werkzeug.utils import secure_filename
import  os
app = Flask(__name__,template_folder='templates',static_folder='static')

db = SQLAlchemy(app)
def url_bind():
    app.add_url_rule('/hello',"hello",hello_world)#add_url_rule 参数，第一个指明路径，第二个指明其他路径跳转到该路径的代替名，本路径的试图函数
    app.add_url_rule('/admin',"admin",hello_admin)
    app.add_url_rule('/user/<name>',"user",hello_name)
    app.add_url_rule('/login',"login",verticate,methods=['POST','GET'])
    app.add_url_rule('/up_load',"up_load",up_load)
    app.add_url_rule('/uploader',"up_loader",uploader,methods=['POST'])

def config_mysql():
    # url的格式为：数据库的协议：//用户名：密码@ip地址：端口号（默认可以不写）/数据库名
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost/project"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    UPLOAD_FOLDER =os.path.curdir+os.path.sep+'uploads'+os.path.sep
    app.config['UPLOAD_FOLDER'] =UPLOAD_FOLDER


class Role(db.Model):

    __tablename__ = "roles"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(16),unique=True)
    # 给Role类创建一个uses属性，关联users表。
    # backref是反向的给User类创建一个role属性，关联roles表。这是flask特殊的属性。
    users = db.relationship('User',backref="role")
    # 相当于__str__方法。
    def __repr__(self):
        return "Role: %s %s" % (self.id,self.name)


class User(db.Model):
    # 给表重新定义一个名称，默认名称是类名的小写，比如该类默认的表名是user。
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(16),unique=True)
    email = db.Column(db.String(32),unique=True)
    password = db.Column(db.String(16))
    # 创建一个外键，和django不一样。flask需要指定具体的字段创建外键，不能根据类名创建外键
    role_id = db.Column(db.Integer,db.ForeignKey("roles.id"))

    def __repr__(self):
        return "User: %s %s %s %s" % (self.id,self.name,self.password,self.role_id)
#
def uploader():#文件上传
    if request.method == 'POST':
        f = request.files['file']
        if f !=None:
           filename =secure_filename(f.filename)
           f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
           return  'file upload successful'
        else:
            return "deafeat"
if __name__ == '__main__':
    # url_bind()
    url_bind()
    config_mysql()
    # ro1 = Role(name="admin")
    # # 先将ro1对象添加到会话中，可以回滚。
    # db.session.add(ro1)
    #
    # ro2 = Role()
    # ro2.name = 'user'
    # db.session.add(ro2)
    # # 最后插入完数据一定要提交
    # db.session.commit()
    # us1 = User(name='wang', email='wang@163.com', password='123456', role_id=ro1.id)
    # us2 = User(name='zhang', email='zhang@189.com', password='201512', role_id=ro2.id)
    # us3 = User(name='chen', email='chen@126.com', password='987654', role_id=ro2.id)
    # us4 = User(name='zhou', email='zhou@163.com', password='456789', role_id=ro1.id)
    # us5 = User(name='tang', email='tang@itheima.com', password='158104', role_id=ro2.id)
    # us6 = User(name='wu', email='wu@gmail.com', password='5623514', role_id=ro2.id)
    # us7 = User(name='qian', email='qian@gmail.com', password='1543567', role_id=ro1.id)
    # us8 = User(name='liu', email='liu@itheima.com', password='867322', role_id=ro1.id)
    # us9 = User(name='li', email='li@163.com', password='4526342', role_id=ro2.id)
    # us10 = User(name='sun', email='sun@163.com', password='235523', role_id=ro2.id)
    # db.session.add_all([us1, us2, us3, us4, us5, us6, us7, us8, us9, us10])
    # db.session.commit()#提交完数据一定commit
    # print("插入ok")
    app.run()
