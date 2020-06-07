from random import randint

from app import app
from flask import render_template, abort, jsonify, request
from couchdb.mapping import Document, TextField, IntegerField, DateTimeField, BooleanField
import couchdb
import json

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'pass'
COUCHDB_URL = 'http://db:5984/'
couch = couchdb.Server(COUCHDB_URL)
# couch.login(ADMIN_USERNAME,ADMIN_PASSWORD)

try:
    db = couch['events']
except couchdb.http.ResourceNotFound:
    db = couch.create('events')

@app.route('/db_handler/get_events', methods=['GET','POST'])
def get_products():
    id = 0
    products = []
    jsonobj = []
    db = couch['events']
    rows = db.view('_all_docs', include_docs=True)
    for each in rows:
        print(each)
        products.append(each)
    return render_template("admin/dashboard.html", feedback="Hmm", retrows=products)

# This is working
@app.route('/db_handler/get_event/', methods=['GET','POST'])
def get_event():
    print("huh")
    if request.method == "POST":

        # Validating the JSON input format
        req = request.form

        missing = list()
        # gets the value from the key value pair and checks if it is empty.
        for k, v in req.items():
            if v == "":
                missing.append(k)

        # if a parameter is missing from the form then the feedback will be passed back to the html page and rendered as such
        if missing:
            feedback = f"Missing identification number!"
            return render_template("admin/get_event_data.html", feedback=feedback)
        try:
            _id = request.form["_id"]
            print(_id)
            db = couch['events']
            event = db[str(_id)]
            successback = f"Found Product"
            print(event)
            return render_template("admin/get_event_data.html", feedback=successback, event=event)
        except couchdb.http.ResourceNotFound:
            feedback = f"Error: Product with that ID does not exist"
            return render_template("admin/get_event_data.html", feedback=feedback)

    return render_template("admin/get_event_data.html", feedback="Hmm")



@app.route('/db_handler/del_event/', methods=['POST'])
def delete_event():

    if request.method == "POST":

        # Validating the JSON input format
        req = request.form

        missing = list()
        # gets the value from the key value pair and checks if it is empty.
        for k, v in req.items():
            if v == "":
                missing.append(k)

        # if a parameter is missing from the form then the feedback will be passed back to the html page and rendered as such
        if missing:
            feedback = f"Missing identification number!"
            return render_template("admin/del_event_data.html", feedback=feedback)
        try:
            _id = request.form["_id"]
            db = couch['events']
            event = db[str(_id)]
            db.delete(event)
            feedback = f"Product successfully deleted"
            print(event)
            return render_template("admin/del_event_data.html", feedback=feedback)
        except couchdb.http.ResourceNotFound:
            feedback = f"Error: Product with that ID does not exist"
            return render_template("admin/del_event_data.html", feedback=feedback)

    return render_template("admin/del_event_data.html", feedback="Hmm")

class Event(Document):
    name = TextField()
    id = TextField()
    description = TextField()
    location = TextField()
    done = BooleanField()

@app.route('/db_handler/create_event', methods=['GET','POST'])
def create_event():
    if request.method == "POST":

        # Validating the JSON input format
        req = request.form

        missing = list()
        # gets the value from the key value pair and checks if it is empty.
        for k, v in req.items():
            if v == "":
                missing.append(k)

        # if a parameter is missing from the form then the feedback will be passed back to the html page and rendered as such
        if missing:
            feedback = f"Missing fields for {', '.join(missing)}"
            return render_template("admin/manage_booking.html", feedback=feedback)

        event = {
            'title': request.form["title"],
            '_id': request.form["_id"],
            'description': request.form["description"],
            'location': request.form["location"],
        }

        db = couch['events']

        try:
            db.save(event)
        except couchdb.http.ResourceNotFound:
            feedback = f"Error: Product with that ID exists in the database"
            return render_template("admin/manage_booking.html", feedback=feedback)
        except couchdb.http.ResourceConflict:
            feedback = f"Error: Product with that ID exists in the database"
            return render_template("admin/manage_booking.html", feedback=feedback)

        # If all parameters are present then the successback variable will create a Success text.
        successback = f"Successful Request, product added!"
        return render_template("admin/manage_booking.html", feedback=successback)


