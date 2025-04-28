from flask import *
from database import*

api=Blueprint('api',__name__)

@api.route('/login_api')
def login_api():
    data={}
    username=request.args['username']
    password=request.args['password']
    a="select * from login where username='%s' and password='%s'"%(username,password)
    b=select(a)
    if b:
        data['status']="success"
        data['data']=b
    else:
        data['status']="failed"
    return str(data)

@api.route('/user_view_mechanic')
def user_view_mechanic():
    data={}
    a="select * from mechanic"
    b=select(a)
    if b:
        data['status']="success"
        data['data']=b
    else:
        data['status']="failed"
    data['method']="view_mech"
    return str(data)

@api.route('/user_view_fuel')
def user_view_fuel():
    data={}
    a="select * from fuel_provider"
    b=select(a)
    if b:
        data['status']="success"
        data['data']=b
    else:
        data['status']="failed"
    data['method']="view_fuel"
    return str(data)

@api.route('/user_send_feedback')
def user_send_feedback():
    data={}
    lid=request.args['lid']
    rating=request.args['rating']
    feedback=request.args['feedback']
    mid=request.args['mid']
    a="insert into feedback values(null,(select user_id from user where login_id='%s'),'%s','%s','%s',curdate())"%(lid,mid,feedback,rating)
    b=insert(a)
    if b:
        data['status']="success"
        data['data']=b
    else:
        data['status']="failed"
    data['method']="add"
    return str(data)


@api.route('/user_send_complaint')
def user_send_complaint():
    data={}
    title=request.args['title']
    complaint=request.args['complaint']
    lid=request.args['lid']
   
    a="insert into complaint values(null,(select user_id from user where login_id='%s'),'%s','%s','pending',curdate())"%(lid,title,complaint)
    b=insert(a)
    if b:
        data['status']="success"
        data['data']=b
    else:
        data['status']="failed"
    data['method']="send"
    return str(data)


@api.route('/user_view_reply')
def user_view_reply():
    data={}
    lid=request.args['lid']
    a="select * from complaint where user_id=(select user_id from user where login_id='%s')"%(lid)
    b=select(a)
    if b:
        data['status']="success"
        data['data']=b
    else:
        data['status']="failed"
    data['method']="view_reply"
    return str(data)


@api.route('/user_mechanic_request')
def user_mechanic_request():
    data={}
    type=request.args['type']
    des=request.args['des']
    lid=request.args['lid']
    lati=request.args['lati']
    longi=request.args['longi']
    mid=request.args['mid']
    a="insert into request values(null,(select user_id from user where login_id='%s'),(select login_id from mechanic where mechanic_id='%s','0'),'%s','%s',curdate(),'pending','%s','%s','pending')"%(lid,mid,type,des,lati,longi)
    b=insert(a)
    if b:
        data['status']="success"
        data['data']=b
    else:
        data['status']="failed"
    data['method']="send"
    return str(data)

@api.route('/user_view_mechanic_request')
def user_view_mechanic_request():
    data={}
    lid=request.args['lid']
    mid=request.args['mech_id']
    a="SELECT * FROM `request` INNER JOIN login ON login.login_id=request.`receiver_id` WHERE user_id=(select user_id from user where login_id='%s') AND usertype='mechanic' AND receiver_id=(select login_id from mechanic where mechanic_id='%s')"%(lid,mid)
    b=select(a)
    if b:
        data['status']="success"
        data['data']=b
    else:
        data['status']="failed"
    data['method']="view_req"
    return str(data)



@api.route('/user_fuel_request')
def user_fuel_request():
    data={}
    type=request.args['type']
    des=request.args['des']
    lid=request.args['lid']
    lati=request.args['lati']
    longi=request.args['longi']
    fid=request.args['fid']
    a="insert into request values(null,(select user_id from user where login_id='%s'),(select login_id from fuel_provider where fuel_provider_id='%s'),'%s','%s',curdate(),'pending','%s','%s','pending','0')"%(lid,fid,type,des,lati,longi)
    b=insert(a)
    if b:
        data['status']="success"
        data['data']=b
    else:
        data['status']="failed"
    data['method']="send"
    return str(data)

@api.route('/user_view_fuel_request')
def user_view_fuel_request():
    data={}
    lid=request.args['lid']
    fid=request.args['fuel_id']
    a="SELECT * FROM `request` INNER JOIN login ON login.login_id=request.`receiver_id` WHERE user_id=(select user_id from user where login_id='%s') AND usertype='fuel' AND receiver_id=(select login_id from fuel_provider where fuel_provider_id='%s')"%(lid,fid)
    b=select(a)
    if b:
        data['status']="success"
        data['data']=b
    else:
        data['status']="failed"
    data['method']="view_req"
    return str(data)

@api.route('/user_mechanic_payment')
def user_mechanic_payment():
    data={}

    amt=request.args['amt']
    rid=request.args['rid']
    a="insert into payment values(null,'%s','%s',curdate(),'Paid')"%(rid,amt)
    b=insert(a)
    if b:
        c="update request set request_amount='%s' where request_id='%s'"%(amt,rid)
        d=update(c)
        if d:
            data['status']="success"
            data['data']=b
        else:
            data['status']="failed"
        data['method']="user_pay"

    return str(data)

@api.route('/user_fuel_payment')
def user_fuel_payment():
    data={}

    amt=request.args['amt']
    rid=request.args['rid']
    a="insert into payment values(null,'%s','%s',curdate(),'Paid')"%(rid,amt)
    b=insert(a)
    if b:
        c="update request set request_amount='%s' where request_id='%s'"%(amt,rid)
        d=update(c)
        if d:
            data['status']="success"
            data['data']=b
        else:
            data['status']="failed"
        data['method']="user_pay"

    return str(data)

@api.route('/mechanic_profile')
def mechanic_profile():
    data={}

    
    lid=request.args['lid']
    a="select * from mechanic where login_id='%s'"%(lid)
    b=select(a)
    if b:
        data['status']="success"
        data['data']=b
    else:
        data['status']="failed"
    data['method']="profile"

    return str(data)

@api.route('/mechanic_view_value')
def mechanic_view_value():
    data={}
    id=request.args['id']
    a="select * from mechanic where login_id='%s'"%(id)
    b=select(a)
    if b:
        data['status']="success"
        data['data']=b
    else:
        data['status']="failed"
    data['method']="view_mech"
        
    return str(data)


@api.route('/mechanic_edit_profile')
def mechanic_edit_profile():
    data={}
    fname=request.args['fname']
    lname=request.args['lname']
    phn=request.args['phn']
    email=request.args['email']
    place=request.args['place']
    id=request.args['id']
    a="update mechanic set mech_fname='%s',mech_lname='%s',mech_place='%s',mech_phone='%s',mech_email='%s' where login_id='%s'"%(fname,lname,place,phn,email,id)
    b=update(a)
    if b:
        data['status']="success"
        data['data']=b
    else:
        data['status']="failed"
    data['method']="update"
        
    return str(data)

@api.route('/mechanic_view_req')
def mechanic_view_req():
    data={}
    id=request.args['lid']
    a="select * from request where receiver_id='%s'"%(id)
    b=select(a)
    if b:
        data['status']="success"
        data['data']=b
    else:
        data['status']="failed"
    data['method']="req"
        
    return str(data)

    

@api.route('/mechanic_view_user')
def mechanic_view_user():
    data={}
    rid=request.args['rid']
    a="SELECT * FROM `request` INNER JOIN `user` USING(user_id) where request_id='%s'"%(rid)
    b=select(a)
    if b:
        data['status']="success"
        data['data']=b
    else:
        data['status']="failed"
    data['method']="user"
        
    return str(data)

@api.route('/mechanic_update_work')
def mechanic_update_work():
    data={}
    rid=request.args['rid']
    stat=request.args['stat']
    a="update request set request_status='%s' where request_id='%s'"%(stat,rid)
    b=update(a)
    if b:
        data['status']="success"
        data['data']=b
    else:
        data['status']="failed"
    data['method']="req_status"
        
    return str(data)

@api.route('/mechanic_view_feedback')
def mechanic_view_feedback():
    data={}
    lid=request.args['lid']

    a="select * from feedback where mechanic_id=(select mechanic_id from mechanic where login_id='%s')"%(lid)
    b=select(a)
    if b:
        data['status']="success"
        data['data']=b
    else:
        data['status']="failed"
    data['method']="feed"
        
    return str(data)

    

@api.route('/fuel_profile')
def fuel_profile():
    data={}
    id=request.args['lid']
    a="select * from fuel_provider where login_id='%s'"%(id)
    b=select(a)
    if b:
        data['status']="success"
        data['data']=b
    else:
        data['status']="failed"
    data['method']="view_fuel"
        
    return str(data)



@api.route('/fuel_view_value')
def fuel_view_value():
    data={}
    id=request.args['id']
    a="select * from fuel_provider where login_id='%s'"%(id)
    b=select(a)
    if b:
        data['status']="success"
        data['data']=b
    else:
        data['status']="failed"
    data['method']="view_fuel"
        
    return str(data)


@api.route('/fuel_edit_profile')
def fuel_edit_profile():
    data={}
    fname=request.args['fname']
    phn=request.args['phn']
    email=request.args['email']
    place=request.args['place']
    id=request.args['id']
    a="update fuel_provider set provider_name='%s',provider_place='%s',provider_phone='%s',provider_email='%s' where login_id='%s'"%(fname,place,phn,email,id)
    b=update(a)
    if b:
        data['status']="success"
        data['data']=b
    else:
        data['status']="failed"
    data['method']="update"
        
    return str(data)

@api.route('/fuel_view_request')
def fuel_view_request():
    data={}
    id=request.args['lid']
    a="select * from request where receiver_id='%s'"%(id)
    b=select(a)
    if b:
        data['status']="success"
        data['data']=b
    else:
        data['status']="failed"
    data['method']="req"
        
    return str(data)


@api.route('/fuel_accept_request')
def fuel_accept_request():
    data={}
    id=request.args['rid']
    a="update request set request_status='Accept' where request_id='%s'"%(id)
    b=update(a)
    if b:
        data['status']="success"
        data['data']=b
    else:
        data['status']="failed"
    data['method']="accept"
        
    return str(data)


@api.route('/fuel_reject_request')
def fuel_reject_request():
    data={}
    id=request.args['rid']
    a="update request set request_status='Reject' where request_id='%s'"%(id)
    b=update(a)
    if b:
        data['status']="success"
        data['data']=b
    else:
        data['status']="failed"
    data['method']="reject"
        
    return str(data)

@api.route('/fuel_view_payment')
def fuel_view_payment():
    data={}
    id=request.args['lid']
    a="SELECT * FROM payment INNER JOIN `request` USING(request_id) where receiver_id='%s'"%(id)
    b=select(a)
    if b:
        data['status']="success"
        data['data']=b
    else:
        data['status']="failed"
    data['method']="pay"
        
    return str(data)


@api.route('/user_reg')
def user_reg():
    data={}
    fame=request.args['fame']
    lname=request.args['lname']
    place=request.args['place']
    phone=request.args['phone']
    email=request.args['email']
    uname=request.args['uname']
    password=request.args['password']
    a="insert into login values(null,'%s','%s','user')"%(uname,password)
    b=insert(a)
    c="insert into user values(null,'%s','%s','%s','%s','%s','%s')"%(b,fame,lname,place,phone,email)
    d=insert(c)
    if d:
        data['status']="success"
        data['data']=d
    else:
        data['status']="failed"
    data['method']="user"
    return str(data)


@api.route('/fuel_reg')
def fuel_reg():
    data={}
    fame=request.args['fame']
 
    place=request.args['place']
    phone=request.args['phone']
    email=request.args['email']
    uname=request.args['uname']
    password=request.args['password']
    lati=request.args['lati']
    longi=request.args['longi']
    a="insert into login values(null,'%s','%s','pending')"%(uname,password)
    b=insert(a)
    c="insert into fuel_provider values(null,'%s','%s','%s','%s','%s','%s','%s')"%(b,fame,place,phone,email,lati,longi)
    d=insert(c)
    if d:
        data['status']="success"
        data['data']=d
    else:
        data['status']="failed"
    data['method']="fuel"
    return str(data)


@api.route('/mech_reg')
def mech_reg():
    data={}
    fame=request.args['fame']
    lname=request.args['lname']
 
    place=request.args['place']
    phone=request.args['phone']
    email=request.args['email']
    uname=request.args['uname']
    password=request.args['password']
    lati=request.args['lati']
    longi=request.args['longi']
    a="insert into login values(null,'%s','%s','pending')"%(uname,password)
    b=insert(a)
    c="insert into mechanic values(null,'%s','%s','%s','%s','%s','%s','%s','%s')"%(b,fame,lname,place,phone,email,lati,longi)
    d=insert(c)
    if d:
        data['status']="success"
        data['data']=d
    else:
        data['status']="failed"
    data['method']="mech"
    return str(data)


