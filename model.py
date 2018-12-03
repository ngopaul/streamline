from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    shape = db.Column(db.String(5)) # circle or quad
    kind = db.Column(db.String(20)) # dining, bar, etc.
    x_pos = db.Column(db.Integer)
    y_pos = db.Column(db.Integer)
    seats = db.Column(db.Integer)
    people = db.Column(db.Integer)
    state = db.Column(db.Integer) # 0 - 4, clean empty, deciding on order, eating, need cleanup, in service, out of service
    states = {0: "empty", 1: "ordering", 2: "dining", 3: "needs cleanup", 4: "in service", 5: "out of service"}
    last_time = db.Column(db.DateTime) # the time the current state started
    orders = db.relationship('Order', backref='table', lazy=True)
    employee = db.relationship('Employee', uselist=False, backref='table')

    def __repr__(self):
        return 'ID %s: %s/%s people\nCurrently %s.' % self.id, self.people, self.seats, self.states[self.state]

    def location(self):
        return self.x, self.y

class Floor(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    vertices = db.Column(db.Text) # 0,0 20,0 20,30 30,0 
    kind = db.Column(db.String(20)) # carpet, linoleum etc
    tables = db.relationship('Table', backref='floor', lazy=True)

    def __repr__(self):
        return self.id

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    value = db.Column(db.Float)
    creditcard = db.Column(db.Text)
    names = db.Column(db.Text)
    employee = db.relationship('Employee', uselist=False, backref='table')

    def conv_names(self):
        return str(self.names).replace(" ", " and ")

    def __repr__(self):
        return "%s paid %s" % self.conv_names(), self.value

class EmployeeClocks(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'),
        nullable=False)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    clocks = db.relationship('EmployeeClocks', backref='employee')
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'),
        nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'),
        nullable=False)

