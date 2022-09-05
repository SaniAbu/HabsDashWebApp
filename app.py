import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy.sql import func
from sqlalchemy import create_engine
import pandas as pd
import sqlite3

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'web_data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Dashers(db.Model):
    DasherID = db.Column(db.String(100), primary_key=True)
    House = db.Column(db.String(100), nullable=False)
    Year = db.Column(db.Integer, nullable=False)
    Streak = db.Column(db.Integer, nullable=False)
    TotalKm = db.Column(db.Float)


class Runs(db.Model):
    DasherID = db.Column(db.String(100), primary_key=True)
    Date = db.Column(db.String(100), nullable=False, primary_key=True)
    RunNo = db.Column(db.Integer, nullable=False)
    Pos = db.Column(db.Integer, nullable=False)
    Time = db.Column(db.String(100), nullable=False)
    pb = db.Column(db.Integer, nullable=False)

engine=create_engine('sqlite:///web_data.db',echo=False)

def create_table():
    runs_csv = pd.read_csv('csvs/rundata.csv')
    dashers_csv = pd.read_csv('csvs/dasherdata.csv')

    runs_csv=runs_csv.values.tolist()
    dashers_csv=dashers_csv.values.tolist()

    conn=engine.connect()

    for row in runs_csv:
        ins=db.insert(Runs).values(DasherID=row[0], Date=row[1], RunNo=row[2], Pos=row[3], Time=row[4], pb=row[5])
        conn.execute(ins)

    for row in dashers_csv:
        ins=db.insert(Dashers).values(DasherID=row[0], House=row[1], Year=row[2], Streak=row[3], TotalKm=row[4])
        conn.execute(ins)

    conn.close()

#create_table()

@app.route("/")
def home():
    runs = Runs.query.all()
    dashers = Dashers.query.all()
    return render_template("home.html", runs=runs, dashers=dashers)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/<string:dasher_id>/')
def dasher(dasher_id):
    dashers = Dashers.query.filter(Dashers.DasherID == str(dasher_id))
    runs = Runs.query.filter(Runs.DasherID == str(dasher_id))
    return render_template('dasher.html', dashers=dashers, runs=runs)

if __name__ == "__main__":
    app.run(debug=True)
