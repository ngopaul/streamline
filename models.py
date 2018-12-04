from app import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    menu_items = db.relationship('MenuItem', backref='Category', lazy=True)

    def __repr__(self):
        return self.name

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), unique=True, nullable=False) 
    items = db.relationship('MenuItem', backref='Menu', lazy=True)

    def __repr__(self):
        return self.name
    

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    normal_price = db.Column(db.Float, unique=False, nullable=False)
    happy_hour_price = db.Column(db.Float, unique=False, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=False)
    # Front-end: Convert input list into long string, where each modifier is separated by spaces
    modifiers = db.Column(db.Text, unique=False, nullable=False) 
    order_items = db.relationship('OrderItem', backref='MenuItem', lazy=True)

    def __repr__(self):
        return self.name + ": " + self.normal_price

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'), nullable=False)
    order_items = db.relationship('OrderItem', backref='Order', lazy=True)

    def __repr(self):
        return "Order " + str(self.id)

class OrderItems(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    menu_item_id = db.Column(db.Integer)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    modifiers = db.Column(db.Text, unique=False, nullable=False)

    def __repr(self):
        return "Order Item" + str(self.id)

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
    size = db.Column(db.Integer)
    seats = db.Column(db.Integer)
    people = db.Column(db.Integer)
    state = db.Column(db.Integer) # 0 - 4, clean empty, deciding on order, eating, check, need cleanup, in service, out of service
    states = {0: "empty", 1: "ordering", 2: "dining", 3: "needs cleanup", 4: "in service", 5: "out of service"}
    last_time = db.Column(db.DateTime) # the time the current state started
    order = db.relationship('Order', uselist=False, backref='table', lazy=True)
    employee = db.relationship('Employee', uselist=False, backref='table')
    floor_id = db.Column(db.Integer, db.ForeignKey('floor.id'),
        nullable=False)

    def __repr__(self):
        return 'ID %s: %s/%s people\nCurrently %s.' % self.id, self.people, self.seats, self.states[self.state]

    def location(self):
        return self.x, self.y

    def info(self):
        return {
            "id" : self.id,
            "shape" : self.shape,
            "kind" : self.kind,
            "x_pos" : self.x_pos,
            "y_pos" : self.y_pos,
            "seats" : self.seats,
            "people" : self.people,
            "state" : self.state,
            "last_time" : self.last_time,
            "orders" : self.orders,
            "employee" : self.employee,
            "floor_id" : self.floor_id,
        }

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
    timestamp = db.Column(db.DateTime, nullable=False, unique=False)
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

