from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from flask_mail import Mail, Message
from decouple import config

# Load email username and passwords
EMAIL_USERNAME = config('MAIL_USERNAME')
EMAIL_PASSWORD = config('MAIL_PASSWORD')
RECIPENT_EMAIL = config('EMAIL_USERNAME')

# Load MongoDB URI
MONGO_URI = config('MONGO_URI')

app = Flask(__name__)

app.config['MONGO_URI'] = MONGO_URI

app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587  # TLS
app.config['MAIL_USERNAME'] = EMAIL_USERNAME
app.config['MAIL_PASSWORD'] = EMAIL_PASSWORD  
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'izzynex23@outlook.com'

mail = Mail(app)
mongo = PyMongo(app)

with app.app_context():
    mail.init_app(app)

# Define a route to the homepage
@app.route("/")
def homepage():
    return render_template("index.html")

# Define a route to handle the contact form
@app.route("/contact", methods=['POST'])
def contact():
    """
    This function handles the contact form submission. It retrieves the form data, stores it in MongoDB, 
    and sends an email to the recipient using Flask-Mail. If the email is sent successfully, it redirects 
    the user to the homepage. Otherwise, it returns an error message.
    """
    if request.method == "POST":
        name = request.form['name'] 
        email = request.form['email']
        subject = request.form['subject']
        messagebody = request.form['message']

        message = Message(subject=subject, recipients=[RECIPENT_EMAIL])

        message.sender = 'izzynex23@outlook.com'

        # msg = Message(subject=f"Mail from {name}", recipients=['izzynex23@outlook.com'])
        message.body = f"Name: {name}\nE-mail: {email}\nSubject: {subject}\nMessage: {messagebody}"

        # Store the data in MongoDB
        collection = mongo.db.Contact_Details
        entry = {
            'name': name,
            'email': email,
            'message': messagebody
        }
        collection.insert_one(entry)

        
        try:
            # Send the email
            mail.send(message)
            return redirect(url_for('homepage'))
        except Exception as e:
            return f"Email not sent. Error: {str(e)}"
        
    return 'Data submitted successfully!'

if __name__ == '__main__':
    app.secret_key = 'your_secret_key' 
    app.run(debug=True)
