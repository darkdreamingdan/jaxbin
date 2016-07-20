from flask import Flask
from flask import url_for, render_template, redirect, session, request, abort, jsonify, Response
from models import *
from urlparse import urlparse
from dicttoxml import dicttoxml
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
    

# The page displayed in an iframe for an embed
@app.route("/embed/<bin_id>",methods=['GET'])
def showBinEmbed(bin_id):
    bin_obj = Bin.select().where(Bin.p_id == bin_id).first()

    return render_template("show_paste.html", paste=bin_obj)
    
# The response for an oEmbed consumer request in XML/JSON 
@app.route("/oembed",methods=['GET'])
def oembedConsumerRequest():
    url = request.args.get("url")
    format = request.args.get("format") or "json"
    maxwidth = int(request.args.get("maxwidth")) if request.args.get("maxwidth") else None
    maxheight = int(request.args.get("maxheight")) if request.args.get("maxheight") else None
    
    scheme = urlparse(url).scheme
    if scheme != "http" and scheme != "https":
        abort(400, "Invalid URL specified")
    
    response = {
        'type' : 'rich',
        'version' : 1.0,
        'provider_name' : 'JaxBin',
        'provider_url' : request.headers['Host'],
        'html' : render_template("show_paste.html"),
        'width' : 0,
        'height' : 0
    }
    
    if request.args.get("format") == "xml":
        response = Response(dicttoxml(response,attr_type=False,custom_root="oembed"), mimetype='text/xml')
    else:
        response = jsonify(response)
    
    return response



# Open & close db connections
@app.before_request
def _db_connect():
    db.connect()

@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()
