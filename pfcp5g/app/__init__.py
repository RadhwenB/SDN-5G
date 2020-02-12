from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app.utils import toBytes
from flask import g

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sdn5g.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)

dt = datetime.today()  # Get timezone naive no
StartUpTimeStamp=toBytes(int (dt.strftime("%s")),4)
print('Getting StartUpTimeStamp ... Done !')

with app.app_context():
    from . import routes
    from . import models
    db.init_app(app)
    db.create_all()
