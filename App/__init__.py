
## See GooldOldBread for more settings

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

#Create the Flask instance for the app
app = Flask(__name__)
Bootstrap(app)

#Read config file for flask extension
app.config.from_object('config')

#create db handler
db = SQLAlchemy(app)



#the App below is the diretory where we store the file (like a module)
# It seems that it must also be the last line to avoid circular import
from App import views, models
