from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

""" app routes """

@app.route('/')
def hello_world():
    return 'Hello, World!'








""" TABLES UI """

""" Makes a new table of kind KIND on the specified FLOOR. """
def make_table(kind, floor_id):
    

if __name__=="__main__":
    app.run(threaded=True)