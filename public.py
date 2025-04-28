from flask import *
from database import*
from detect import *

# import uuid

public=Blueprint('public',__name__)

@public.route('/')
def home():
    return render_template('home.html')
    

@public.route('/login',methods=['post','get'])
def login():
    if 'submit' in request.form:
        uname=request.form['uname']
        pwd=request.form['password']
        a="select * from login where username='%s' and password='%s'"%(uname,pwd)
        b=select(a)
        session['log']=b[0]['login_id']
        if b[0]['usertype']=='admin':
            return redirect(url_for("admin.admin_home"))
        
        # if b[0]['usertype']=='pumb':
        #     c="select * from petrol_pumb where login_id='%s'"%(session['log'])
        #     d=select(c)
        #     if d:
        #         session['pumb']=d[0]['pumb_id']
        #         session['email']
        #         return redirect(url_for("pumb.pumb_home"))
        
       
    
    return render_template('login.html')


@public.route('/ca')
def ca():
    d=detect(1)
    
    return render_template("home.html")
