from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from flask_mail import Mail
with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)
app.secret_key = 'super-secret-key'

app.config.update(
    MAIL_SERVER ='smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']

)
mail =Mail(app)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']

else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = True
db = SQLAlchemy(app)
@app.route("/", methods =['GET', 'POST'])
def home():

    if (request.method == 'POST'):
        '''
        add entry to database
        '''

        class Contact(db.Model):
            '''
            sno, name, phone, msg , date, email.
            '''
            sno = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(80), unique=False, nullable=False)
            email = db.Column(db.String(20), nullable=False)
            phone = db.Column(db.String(12), nullable=False)
            msg = db.Column(db.String(120), nullable=False)
            date = db.Column(db.String(12), nullable=True)

        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        entry = Contact(name=name, phone=phone, msg=message, email=email, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name,
                          sender=email,
                          recipients=[params['gmail-user']],
                          body= "Their message is: "+message + "\n" +"Mobile number: "+ phone)
        mail.send_message('Thank You for contacting me ' + name,
                          sender=params['gmail-user'],
                          recipients=[email],
                          body=" I really appreciate your time to visit my website and contacting me. I will get back to you very soon."+"\n"+" Regards"+"\n""Anuj Patel")
    return render_template('index.html', params=params)


app.run(debug=True)
