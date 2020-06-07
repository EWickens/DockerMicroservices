from app import app
from flask import render_template, abort, jsonify, request, redirect


@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin/dashboard.html")

@app.route("/admin/get_event_data")
def get_event_data():
    return render_template("admin/get_event_data.html")

@app.route("/admin/del_event_data")
def del_event_data():
    return render_template("admin/del_event_data.html")

@app.route("/admin/manage_booking", methods=["GET", "POST"])
def manage_booking():
    return render_template("/admin/manage_booking.html")


