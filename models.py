from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


class Marksupdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    marks = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(1), nullable=False)

    def __init__(self, name, marks):
        self.name = name
        self.marks = marks
        self.grade = self.calculate_grade()

    def calculate_grade(self):

        if self.marks <= 40:
            return "C"

        elif self.marks <= 80:
            return "B"

        else:
            return "A"

    def __repr__(self):
        return f"Marksupdate('{self.name}', '{self.marks}', '{self.grade}')"


with app.app_context():
    db.create_all()


# CREATE
@app.route('/data/create', methods=['GET', 'POST'])
def create():

    if request.method == 'GET':
        return render_template('create.html')

    if request.method == 'POST':

        name = request.form['name']
        marks = int(request.form['marks'])

        new_marksupdate = Marksupdate(name, marks)

        db.session.add(new_marksupdate)
        db.session.commit()

        return redirect('/data')


# RETRIEVE ALL
@app.route('/data')
def RetrieveDataList():

    all_data = Marksupdate.query.all()

    return render_template('datalist.html', marksupdate=all_data)


# RETRIEVE SINGLE
@app.route('/data/<int:id>')
def RetrieveData(id):

    data = Marksupdate.query.get_or_404(id)

    return render_template('data.html', marksupdate=data)


# UPDATE
@app.route('/data/<int:id>/update', methods=['GET', 'POST'])
def update(id):

    data = Marksupdate.query.get_or_404(id)

    if request.method == 'POST':

        data.name = request.form['name']
        data.marks = int(request.form['marks'])

        # recalculate grade
        if data.marks <= 40:
            data.grade = "C"

        elif data.marks <= 80:
            data.grade = "B"

        else:
            data.grade = "A"

        db.session.commit()

        return redirect('/data')

    return render_template('update.html', marksupdate=data)


# DELETE
@app.route('/data/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):

    data = Marksupdate.query.get_or_404(id)

    if request.method == 'POST':

        db.session.delete(data)
        db.session.commit()

        return redirect('/data')

    return render_template('delete.html', marksupdate=data)


app.run(host="localhost",port=5000,debug=True)