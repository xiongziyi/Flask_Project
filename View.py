from flask import Flask,redirect,url_for,request,render_template
from werkzeug import  security
from werkzeug.utils import secure_filename
import os
from app import  app
UPLOAD_FOLDER =os.path.curdir+os.path.sep+'uploads'+os.path.sep

def hello_world():

    return  render_template('Logins.html')

def hello_name(name):#变量使用
   return 'Hello %s!' % name


def hello_admin():
    context={
        'username':"王亚锋",
        'age': "18",
        'gender': "男",
        'flag': "王者",
        'hero': "猴子",
        'wwwurl':{
            'baidu':'www.baidu.com',
            'google':'www.google.com'
        }
    }
    datas = ['100', '100', '100', '100', '100']
    return  render_template('login.html',data = datas,**context,context=context)#常见传值类型

def hello_user(name):
    if(name =='admin'):
        return  redirect(url_for('admin'))
    else:
        return  redirect(url_for('user',name = name))

def verticate():
    if request.method == 'POST':
        error = None
        user = request.form['name']
        password = request.form['password']
        if(len(password)>7):
          return  redirect(url_for('up_load'))
        else:
            error = 'Invalid username or password. Please try again!'
            return  redirect(url_for('hello',error = error))
    else:
        user= request.args.get('nm')
        user = user +"get"
        return redirect(url_for('user',name=user))


def  up_load():
    return  render_template("upload_file.html")

# def uploader():
#     if request.method == 'POST':
#         f = request.files['file']
#         if f !=None:
#            filename =secure_filename(f.filename)
#            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#            return  'file upload successful'
#         else:
#             return "deafeat"