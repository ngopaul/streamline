from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import models
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

""" app routes """

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

#region TABLE

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

""" Returns a list of table_info_list. """
def table_read(info = []):
    return [table.info() for table in models.Table.query.all()]

""" Updates a table according to information in info. """
def table_update(info):
    [id, x_pos, y_pos, size, seats, people, state, new_orderitem, delete_orderitem] = info
    # new_orderitem looks like: [menuitemid, modifiers]
    # delete_orderitem looks like: orderid
    # table = User.query.filter_by(id=id).first()
    table = models.Table.query.filter_by(id=id).first()
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
        orderitem = models.OrderItem(order_id=table.order.id, menu_item_id=new_orderitem[0], modifiers=new_orderitem[1])
        db.session.add(orderitem)
        db.session.commit()
        return orderitem.id
    elif delete_orderitem:
        models.OrderItem.query.filter_by(id=delete_orderitem).delete()
    db.session.commit()
    return info

""" Deletes a table of a certain ID. """
def table_delete(ID):
    models.Table.query.filter_by(id=ID).delete()
    db.session.commit()

#endregion TABLE

#region FLOOR

""" Creates a new FLOOR. """
def floor_create(info):
    vertices = info # vertices is a string of x y pairs: 0,0 20,0 20,30 30,0 
    floor = models.Floor(vertices=vertices)
    db.session.add(floor)
    db.session.commit()
    return floor.id

""" Returns a list of floor_info s. """
def floor_read(info = []):
    return [floor.info() for floor in models.Floor.query.all()]

""" Updates a FLOOR by changing its type, or vertices. Multiple changes can be done at once. """
def floor_update(info):
    # info = [material, kind, vertices]
    [id, material, kind, vertices] = info
    # floor = User.query.filter_by(id=id).first()
    floor = models.Floor.query.filter_by(id=id).first()
    floor.material = material
    floor.kind = kind
    floor.vertices = vertices
    db.session.commit()
    return info

""" Deletes a FLOOR, and all the TABLEs on it. """ 
def floor_delete(ID):
    models.Floor.query.filter_by(id=ID).delete()
    models.Table.filter_by(floor_id=ID).delete()
    db.session.commit()

#endregion FLOOR

#region ORDER

""" Creates a new ORDER. ORDERs do not contain any ORDERITEMs by default. """
def order_create(info):
    [table_id, to_go] = info
    if to_go:
        order = models.Order(to_go = to_go)
    else:
        order = models.Order(table_id = table_id, to_go = to_go)
    db.session.add(order)
    db.session.commit()
    return order.id

""" Returns a list of order_info s. """
def floor_read(info = []):
    return [order.info() for order in model.Order.query.all()]

""" Updates an ORDER by changing its kind to/from to-go. (if you want to add an ORDERITEM, see the CRUD for ORDERITEM)."""
def order_update(info):
    [id, to_go, table_id] = info
    order = models.Order.query.filter_by(id=id).first()
    if order.to_go and not to_go:
        order.table_id = table_id
    order.to_go = to_go
    db.session.commit()
    return info

""" Deletes an ORDER. Do after saving proper information to disk and customer has paid. """
def order_delete(ID):
    models.Order.query.filter_by(id=ID).delete()
    db.session.commit()

#endregion ORDER

#region ORDERITEM

""" Creates a new ORDERITEM. """
def orderitem_create(info):
    [menu_item_id, order_id, modifiers] = info
    orderitem = models.OrderItem(menu_item_id = menu_item_id, order_id = order_id, modifiers = modifiers)
    db.session.add(orderitem)
    db.session.commit()
    return orderitem.id

""" Returns a list of orderitem info """
def orderitem_read(info = []):
    return [orderitem.info() for orderitem in model.OrderItem.query.all()]

""" Updates an ORDERITEM by changing its modifiers. Other changes would be deletion and creation only."""
def orderitem_update(info):
    [id, modifiers] = info
    orderitem = models.OrderItem.query.filter_by(id=id).first()
    orderitem.modifiers = modifiers
    db.session.commit()
    return info

""" Deletes an ORDERITEM. """
def orderitem_delete(ID):
    models.OrderItem.query.filter_by(id=ID).delete()
    db.session.commit()

#endregion ORDERITEM

commands = {
    'table_create' : table_create
}

if __name__=="__main__":
    app.run(threaded=True)