"""App design"""
import logging.config
import traceback
import re
import os

import sqlalchemy.exc
from flask import Flask, render_template, request
from wtforms import SelectField
from flask_wtf import FlaskForm

from src.add_products import Product, ProductManager

# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

# Configure flask app from flask_config.py
app.config.from_pyfile("config/flaskconfig.py")
SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug(
    "Web app should be viewable at %s:%s if docker run command maps local "
    "port to the same port as configured for the Docker container "
    "in config/flaskconfig.py (e.g. `-p 5000:5000`). Otherwise, go to the "
    "port defined on the left side of the port mapping "
    "(`i.e. -p THISPORT:5000`). If you are running from a Windows machine, "
    "go to 127.0.0.1 instead of 0.0.0.0.", app.config["HOST"]
    , app.config["PORT"])

# Initialize the database session
product_manager = ProductManager(app)


class Form(FlaskForm):
    """Format form for user input"""
    itemid = SelectField("input_itemid", choices=[])


@app.route("/")
def index():
    """Format options for input in form"""
    form = Form()
    form.itemid.choices = [re.sub(r"[^\w]", "", str(itemid)) for itemid in
                           product_manager.session.query(Product.input_itemid).distinct()]
    return render_template("index.html", form=form)


@app.route("/", methods=["POST"])
def data():
    """Format output page with user input"""
    if request.method == "POST":
        input_itemid = request.form.to_dict()["itemid"]
        try:
            products = product_manager.session.query(Product) \
                .filter_by(input_itemid=input_itemid).limit(app.config["MAX_ROWS_SHOW"]).all()
            if len(products) != 0:
                return render_template("recommend.html", products=products,
                                       input_itemid=input_itemid)
            return render_template("error.html")
        except sqlalchemy.exc.OperationalError:
            traceback.print_exc()
            return render_template("error.html")


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
