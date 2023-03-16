from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telephone = db.Column(db.String(100))

    def __init__(self,name,email,telephone):
        self.name = name
        self.email = email
        self.telephone = telephone

@app.route('/')
def index():
    all_data = Data.query.all()
    return render_template("index.html", employees = all_data)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        telephone = request.form['telephone']

        my_data = Data.query.filter((Data.name == name) | (Data.email == email) | (Data.telephone == telephone)).first()
        if my_data:
            if my_data.name == name and my_data.email == email and my_data.telephone == telephone:
                flash("Employee already exists")
            elif my_data.name == name and my_data.email == email:
                flash("Name and email already exist")
            elif my_data.email == email and my_data.telephone == telephone:
                flash("Email and phone number already exist")
            elif my_data.name == name and my_data.telephone == telephone:
                flash("Name and phone number already exist")
            elif my_data.name == name:
                flash("Name already exists")
            elif my_data.email == email:
                flash("Email already exists")
            else:
                flash("Phone number already exists")
            return redirect(url_for('index'))

        my_Data = Data(name, email, telephone)
        db.session.add(my_Data)
        db.session.commit()

        flash("Employee added successfully")

        return redirect (url_for('index'))
    
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.telephone = request.form['telephone']

        db.session.commit()
        flash("Employee Updated Successfully")

        return redirect(url_for('index'))
    
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee deleted successfully")

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=False)