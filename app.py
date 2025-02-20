from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route("/")
def home():
    return "ColTrac test"

if __name__ == "__main__":
    app.run()