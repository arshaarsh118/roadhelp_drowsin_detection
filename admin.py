from flask import *
from database import*
import uuid

admin=Blueprint('admin',__name__)

@admin.route('/admin_home')
def admin_home():
    return render_template('admin_home.html')

@admin.route('/admin_verify_mechanic', methods=['post', 'get'])
def admin_verify_mechanic():
    # if 'submit' in request.form:
    #     name = request.form['name']
    #     place = request.form['place']
    #     phone = request.form['phone']
    #     email = request.form['email']
    #     lati = request.form['lati']
    #     longi = request.form['longi']
    #     uname = request.form['uname']
    #     pwd = request.form['pwd']
    #     certi = request.files['certi']
    #     path = "static/" + str(uuid.uuid4()) + certi.filename
    #     certi.save(path)
        
    #     # Insert into login table
    #     a = "insert into login values(null,'%s','%s','mechanic')" % (uname, pwd)
    #     b = insert(a)
        
    #     # Insert into mechanic table
    #     c = "insert into mechanic values(null,'%s','%s','%s','%s','%s','%s','%s','%s')" % (b, name, place, phone, email, lati, longi, path)
    #     d = insert(c)
        
    #     if d:
    #         # Send email after successful insertion
    #         try:
    #             send_email_mechanic_reg(email, name, uname, pwd, place, phone)
    #             return '''<script>alert("Mechanic Details Added and Email Sent");window.location='/admin_manage_mechanic'</script>'''
    #         except Exception as e:
    #             return '''<script>alert("Mechanic Details Added but Email Failed: %s");window.location='/admin_manage_mechanic'</script>''' % str(e)
    
    data = {}
    e = "select * from mechanic inner join login using(login_id)"
    f = select(e)
    if f:
        data['view'] = f
    
    if 'action' in request.args:
        act = request.args['action']
        id = request.args['lid']
        if act == 'accept':
            g="update login set usertype='mechanic' where login_id='%s'"%(id)
            h=update(g)
            if h:
                 return '''<script>alert("Accepted Successfully");window.location='/admin_verify_mechanic'</script>'''
        if act == 'reject':
            i="update login set usertype='reject' where login_id='%s'"%(id)
            j=update(i)
            if j:
                 return '''<script>alert("Rejected Successfully");window.location='/admin_verify_mechanic'</script>'''
                
        
    return render_template('admin_verify_mechanic.html', data=data)

# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# def send_email_mechanic_reg(to_email, name, username, password, place, phone):
#     try:
#         gmail = smtplib.SMTP('smtp.gmail.com', 587)
#         gmail.ehlo()
#         gmail.starttls()
#         gmail.login('hariharan0987pp@gmail.com', 'rjcbcumvkpqynpep')

#         msg = MIMEMultipart()
#         msg['From'] = 'hariharan0987pp@gmail.com'
#         msg['To'] = to_email
#         msg['Subject'] = 'Mechanic Registration Successful - Welcome On Road Assistance & Fuel !'

#         # Detailed email body with all information
#         body = f"""Dear {name},

# Congratulations! Your mechanic account has been successfully created. Below are your registration details:

# Name: {name}
# Username: {username}
# Password: {password}
# Location: {place}
# Phone Number: {phone}
# Email: {to_email}

# You can now login to the system using your username and password. Please keep your credentials safe and secure.

# For any assistance, feel free to contact our support team at hariharan0987pp@gmail.com.

# Welcome to our mechanic network!

# Best regards,
# The Admin Team
# """

#         msg.attach(MIMEText(body, 'plain'))
#         gmail.send_message(msg)
#         gmail.quit()
#         print("Email sent successfully to", to_email)

#     except smtplib.SMTPException as e:
#         print(f"Failed to send email: {e}")
#         raise




@admin.route('/admin_verify_fuel', methods=['post', 'get'])
def admin_verify_fuel():
    # if 'submit' in request.form:
    #     name = request.form['name']
    #     place = request.form['place']
    #     phone = request.form['phone']
    #     email = request.form['email']
    #     lati = request.form['lati']
    #     longi = request.form['longi']
    #     uname = request.form['uname']
    #     pwd = request.form['pwd']
    #     certi = request.files['certi']
    #     path = "static/" + str(uuid.uuid4()) + certi.filename
    #     certi.save(path)
        
    #     # Insert into login table
    #     a = "insert into login values(null,'%s','%s','pumb')" % (uname, pwd)
    #     b = insert(a)
        
    #     # Insert into petrol_pumb table
    #     c = "insert into petrol_pumb values(null,'%s','%s','%s','%s','%s','%s','%s','%s')" % (b, name, place, phone, email, lati, longi, path)
    #     d = insert(c)
        
    #     if d:
    #         # Send email after successful insertion
    #         try:
    #             send_email_pumb_reg(email, name, uname, pwd, place, phone, lati, longi)
    #             return '''<script>alert("Pump Details Added and Email Sent");window.location='/admin_manage_pumb'</script>'''
    #         except Exception as e:
    #             return '''<script>alert("Pump Details Added but Email Failed: %s");window.location='/admin_manage_pumb'</script>''' % str(e)
    
    data = {}
    e = "select * from fuel_provider inner join login  using(login_id)"
    f = select(e)
    if f:
        data['view'] = f
    
    if 'action' in request.args:
        act = request.args['action']
        id = request.args['lid']
        if act == 'accept':
            g="update login set usertype='fuel' where login_id='%s'"%(id)
            h=update(g)
            if h:
                 return '''<script>alert("Accepted Successfully");window.location='/admin_verify_fuel'</script>'''
        if act == 'reject':
            i="update login set usertype='reject' where login_id='%s'"%(id)
            j=update(i)
            if j:
                 return '''<script>alert("Rejected Successfully");window.location='/admin_verify_fuel'</script>'''

    return render_template('admin_verify_fuel.html', data=data)

# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# def send_email_pumb_reg(to_email, name, username, password, place, phone, latitude, longitude):
#     try:
#         gmail = smtplib.SMTP('smtp.gmail.com', 587)
#         gmail.ehlo()
#         gmail.starttls()
#         gmail.login('hariharan0987pp@gmail.com', 'rjcbcumvkpqynpep')

#         msg = MIMEMultipart()
#         msg['From'] = 'hariharan0987pp@gmail.com'
#         msg['To'] = to_email
#         msg['Subject'] = 'Petrol Pump Registration Successful - Welcome On Road Assistance & Fuel!'

#         # Detailed email body with all information
#         body = f"""Dear {name},

# Congratulations! Your petrol pump has been successfully registered in our system. Below are your registration details:

# Petrol Pump Name: {name}
# Username: {username}
# Password: {password}
# Location: {place}
# Phone Number: {phone}
# Email: {to_email}
# Latitude: {latitude}
# Longitude: {longitude}

# You can now login to the system using your username and password. Please keep your credentials secure and do not share them with anyone.

# For any assistance or queries, feel free to contact our support team at hariharan0987pp@gmail.com.

# Welcome to our petrol pump network! We look forward to a successful partnership.

# Best regards,
# The Admin Team
# """

#         msg.attach(MIMEText(body, 'plain'))
#         gmail.send_message(msg)
#         gmail.quit()
#         print("Email sent successfully to", to_email)

#     except smtplib.SMTPException as e:
#         print(f"Failed to send email: {e}")
#         raise


@admin.route('/admin_view_request')
def admin_view_request():
    data={}
    a="SELECT * FROM `request` INNER JOIN USER USING(user_id) INNER JOIN login ON request.receiver_id=login.login_id"
    b=select(a)
    if b:
        data['view'] = b
    return render_template('admin_view_request.html',data=data)

@admin.route('/admin_view_feedback')
def admin_view_feedback():
    data={}
    a="select * from feedback inner join user using(user_id) inner join mechanic using(mechanic_id)"
    b=select(a)
    if b:
        data['view'] = b
    return render_template('admin_view_feedback.html',data=data)



@admin.route('/admin_view_complaint')
def admin_view_complaint():
    data={}
    a="select * from complaint inner join user using(user_id)"
    b=select(a)
    if b:
        data['view'] = b
    return render_template('admin_view_complaint.html',data=data)


@admin.route('/admin_send_reply', methods=['post', 'get'])
def admin_send_reply():
    cid=request.args['cid']
    if 'submit' in request.form:
        reply=request.form['reply']
        a="update complaint set reply='%s' where complaint_id='%s'"%(reply,cid)
        b=update(a)
        if b:
            return '''<script>alert("Reply Send Successfully");window.location='/admin_view_complaint'</script>'''
    return render_template('admin_send_reply.html')


