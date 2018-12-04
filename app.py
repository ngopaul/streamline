from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import models
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

""" app routes """

commands = {
    'table_create' : table_create
}

def post_to_function(action, info):
    return commands[action](info)

@app.route('/')
def main():
    if request.method == "POST":
        action = request.values.get('action') # table_create, table_delete, etc.
        info = request.value.get('info') # an array that has different info based the fxn
        return_values = post_to_function(action, info) # do the desired action
    elif request.method == "GET":
        return render_template("home.html")
    return render_template("home.html", return_values=return_values)

""" TABLES UI """

""" Makes a new table of kind KIND on the specified FLOOR. """
def table_create(info):
    [kind, shape, floor, x_pos, y_pos, size] = info
    # make a table of a certain kind, shape, floor, location and size. Has 1 seat by default
    table = models.Table(kind=kind, shape=shape, floor_id=floor.id, x_pos=x_pos, y_pos=y_pos, size=size, seats=1, people=0, last_time=datetime.datetime, state=0)
    # make an empty Order
    order = models.Order(table_id=table.id) 
    table.order = order
    db.session.add(table)
    db.session.commit()
    return table.id

def table_read(info = []):
    return [table.info for table in models.Table.query.all()]

def table_update(info):
    [id, x_pos, y_pos, size, seats, people, state, new_orderitem, delete_orderitem] = info
    # new_orderitem looks like: [menuitemid, modifiers]
    # delete_orderitem looks like: orderid
    table = User.query.filter_by(id=id).first()
    table.x_pos = x_pos
    table.y_pos = y_pos
    table.size = size
    table.seats = seats
    table.people = people
    if table.state != state:
        table.last_time = datetime.datetime
        table.state = state
        return table.state
    elif new_orderitem:
        orderitem = models.OrderItems(order_id=table.order.id, menu_item_id=new_order[0], modifiers=new_order[1])
        db.session.add(orderitem)
        db.session.commit()
        return orderitem.id
    elif delete_orderitem:
        models.OrderItems.query.filter_by(id=delete_orderitem).delete()

""" Deletes a table of a certain ID. """
def table_delete(ID):
    models.Table.query.filter_by(id=ID).delete()
    db.session.commit()

if __name__=="__main__":
    app.run(threaded=True)