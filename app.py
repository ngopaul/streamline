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

""" TABLE """

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
    return [table.info for table in models.Table.query.all()]

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
        orderitem = models.OrderItems(order_id=table.order.id, menu_item_id=new_orderitem[0], modifiers=new_orderitem[1])
        db.session.add(orderitem)
        db.session.commit()
        return orderitem.id
    elif delete_orderitem:
        models.OrderItems.query.filter_by(id=delete_orderitem).delete()

""" Deletes a table of a certain ID. """
def table_delete(ID):
    models.Table.query.filter_by(id=ID).delete()
    db.session.commit()

""" FLOOR """

""" Creates a new FLOOR. """
def floor_create(info):
    vertices = info # vertices is a string of x y pairs: 0,0 20,0 20,30 30,0 
    floor = models.Floor(vertices=vertices)
    db.session.add(floor)
    db.session.commit()
    return floor.id

""" Returns a list of floor_info s. """
def floor_read(info = []):
    return [floor.info for floor in models.Floor.query.all()]

""" Updates a floor by changing its type, or vertices. Multiple changes can be done at once. """
def floor_update(info):
    # info = [material, kind, vertices]
    [id, material, kind, vertices] = info
    # floor = User.query.filter_by(id=id).first()
    floor = models.Floor.query.filter_by(id=id).first()
    floor.material = material
    floor.kind = kind
    floor.vertices = vertices
    return info

""" Deletes a floor, and all the tables on it. """ 
def floor_delete(ID):
    models.Floor.query.filter_by(id=ID).delete()
    models.Table.filter_by(floor_id=ID).delete()
    db.session.commit()


commands = {
    'table_create' : table_create
}


if __name__=="__main__":
    app.run(threaded=True)