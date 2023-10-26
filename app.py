from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from config import EMAIL_USERNAME, EMAIL_PASSWORD
from decouple import config

# Load email username and passwords
EMAIL_USERNAME = config('MAIL_USERNAME')
EMAIL_PASSWORD = config('MAIL_PASSWORD')
RECIPENT_EMAIL = config('EMAIL_USERNAME')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root@localhost/personal_portfolio"

app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587  # TLS
app.config['MAIL_USERNAME'] = EMAIL_USERNAME
app.config['MAIL_PASSWORD'] = EMAIL_PASSWORD  
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'izzynex23@outlook.com'

db = SQLAlchemy(app)
mail = Mail(app)

with app.app_context():
    mail.init_app(app)

# Create a model for Contact_Details
class ContactDetails:
    def __init__(self, name, subject, email, message):
        self.name = name
        self.subject = subject
        self.email = email
        self.message = message
class ContactDetails(db.Model):
    # Define your model's fields here
    name = db.Column(db.String(100))
    subject = db.Column(db.String(100))
    email = db.Column(db.String(100), primary_key=True)
    message = db.Column(db.Text)

# Define a route to the homepage
@app.route("/")
def homepage():
    return render_template("index.html")

# Define a route to handle the contact form
@app.route("/contact", methods=['POST'])
def contact():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        messagebody = request.form['message']

        # Store the data in MySQL
        # from models import ContactDetails  # Create a model for Contact_Details
        contact_entry = ContactDetails(name=name, subject=subject, email=email, message=messagebody)
        db.session.add(contact_entry)
        db.session.commit()

        message = Message(subject=subject, recipients=['joelekeng23@gmail.com'])  # Set the recipient's email address
        message.sender = 'izzynex23@outlook.com'
        message.body = f"Name: {name}\nE-mail: {email}\nSubject: {subject}\nMessage: {messagebody}"

        try:
            # Send the email
            mail.send(message)
            return redirect(url_for('homepage'))
        except Exception as e:
            return f"Email not sent. Error: {str(e)}"
        
    return 'Data submitted successfully!'

if __name__ == '__main__':
    app.run(debug=True)
    app.secret_key = 'your_secret_key'  

