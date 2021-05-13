from flask import Flask, render_template, redirect, request, url_for, flash

from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = "SecretKey"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/crud'  #used for connection to db with pass and username
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  #This will remove the warning message in terminal

db = SQLAlchemy(app)

class Emp(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(100), nullable=False)
    email =db.Column(db.String(100), nullable= False)
    phone = db.Column(db.String(100), nullable=False)

    def __init__(self, name, email, phone):
        self.name = name 
        self.email = email
        self.phone = phone
    




@app.route('/')
def Index():
    all_data = Emp.query.all()
    return render_template("index.html", employees = all_data)


@app.route('/insert', methods= ['POST'])
def insert():
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        
        my_data = Emp(name, email, phone)
        db.session.add(my_data)
        db.session.commit()

        flash("Employee inserted successfully!")
        return redirect(url_for('Index'))

@app.route('/update', methods =['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Emp.query.get(request.form.get('id'))
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']

        db.session.commit()
        flash('Employee updated successfully')
        return redirect(url_for('Index'))

@app.route('/delete/<id>/', methods= ['GET', 'POST'])
def delete(id):
    my_data = Emp.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee has been successfully deleted!...")
    return redirect(url_for("Index"))








if __name__ == "__main__":
    app.run(debug=True)