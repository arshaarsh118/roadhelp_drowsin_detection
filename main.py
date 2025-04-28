from flask import *
from database import *
from admin import admin
from public import public

from api import api


app = Flask(__name__)
app.register_blueprint(public)
app.register_blueprint(admin)

app.register_blueprint(api)

app.secret_key = "hihihi"

# Email configuration (corrected for TLS)
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USERNAME'] = 'hariharan0987pp@gmail.com'
# app.config['MAIL_PASSWORD'] = 'rjcbcumvkpqynpep'  # Your App Password
# app.config['MAIL_USE_TLS'] = True  # Enable TLS for port 587
# app.config['MAIL_USE_SSL'] = False  # Disable SSL
# app.config['MAIL_DEFAULT_SENDER'] = 'hariharan0987pp@gmail.com'

# mail = Mail(app)

# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if 'submit' in request.form:
#         uname = request.form['uname']
#         pwd = request.form['pwd']
#         a = "select * from login where username='%s' and password='%s'" % (uname, pwd)
#         b = select(a)
        
#         if b:  # If credentials are correct
#             session['log'] = b[0]['login_id']
            
#             if b[0]['usertype'] == 'admin':
#                 return redirect(url_for("admin.admin_home"))
            
#             elif b[0]['usertype'] == 'pumb':
#                 c = "select * from petrol_pumb where login_id='%s'" % (session['log'])
#                 d = select(c)
#                 print(d, "//////////////////")
#                 if d:
#                     session['pumb'] = d[0]['pumb_id']
#                     session['email'] = d[0]['pumb_email']  # Assuming email is stored in petrol_pumb table
                    
#                     # Generate and store OTP
#                     otp = str(random.randint(100000, 999999))
#                     session['otp'] = otp
                    
#                     # Send OTP via email
#                     msg = Message('Login OTP Verification',
#                                 recipients=[session['email']])
#                     msg.body = f'Your OTP for login is: {otp}'
#                     try:
#                         mail.send(msg)
#                         return redirect(url_for('verify_otp'))  # Changed to direct route since it's in main app
#                     except Exception as e:
#                         print(e, "/////////////")
#                         flash(f'Error sending OTP: {str(e)}')
#                         return render_template('login.html')
#         else:
#             flash('Invalid username or password')
    
#     return render_template('login.html')

# @app.route('/verify_otp', methods=['POST', 'GET'])
# def verify_otp():
#     if 'verify' in request.form:
#         user_otp = request.form['otp']
#         if user_otp == session.get('otp'):
#             # OTP verified successfully
#             session.pop('otp', None)  # Remove OTP from session
#             return redirect(url_for("pumb.pumb_home"))
#         else:
#             flash('Invalid OTP. Please try again.')
    
#     return render_template('verify_otp.html')

# if __name__ == '__main__':

app.run(debug=True, port=5007, host="0.0.0.0")