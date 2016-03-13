from flask import Flask
from flask import url_for, render_template, redirect, session, request, abort
from models import *
import uuid

app = Flask('jaxbin')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/createBin", methods=['GET', 'POST'])
def createBin():
    binData = request.form["binData"]
    bin_id = str(uuid.uuid4())

    Bin.create(
        p_id = bin_id,
        content = binData
    )

    if not binData:
        abort(400, "Invalid Request")

    return bin_id

@app.route("/bin/<bin_id>")
def showBin(bin_id):
    bin_obj = Bin.select().where(Bin.p_id == bin_id).first()

    return render_template("show_paste.html", paste=bin_obj)
