from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# cause i will need this later https://docs.sqlalchemy.org/en/14/core/engines.html#postgresql
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:admin@localhost:5432/test"
db = SQLAlchemy()
db.init_app(app)

#*TO CREATE ALL TABLES
# from opencanvas import models

# with app.app_context():
#     db.create_all()

from opencanvas import routes