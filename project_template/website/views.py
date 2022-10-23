from dataclasses import dataclass
from datetime import datetime
from django.shortcuts import render
from flask import Blueprint, render_template, request, flash, current_app as app, redirect, url_for
from flask_login import login_required, current_user
from .models import Trip
from . import db
import json, os
from .read_trip_suggestions import get_json
import folium

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@views.route('events', methods=['GET', 'POST'])
@login_required
def events():
    if request.method == 'POST':
        if request.form['submit_button'] == 'create trip':
            date_in = request.form.get('tripDate')
            time_in = request.form.get('tripTime')
            name_in = request.form.get('name')
            desc_in = request.form.get('desc')
            tripType_in = request.form.get('tripType')
            num_people_in = request.form.get('num_people')
            date_time = datetime.strptime(date_in + " " + time_in,"%Y-%m-%d %H:%M")
            if len(name_in) < 1:
                flash('Trip name is too short!', category='error')
            else:
                new_trip = Trip(name = name_in, desc = desc_in, trip_type = tripType_in, date = date_time, num_people = num_people_in, user_id=current_user.id)
                db.session.add(new_trip)
                db.session.commit()
                flash('Trip added!', category='success')

    return render_template("events.html", user=current_user)

@views.route('/map')
def index():
    start_coords = (35, -83)
    folium_map = folium.Map(min_zoom = 4, center=start_coords, height = "90%",tiles="Stamen Terrain")
    return folium_map._repr_html_()

@views.route('/profile/', methods = ['GET', 'POST'])
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@views.route('suggestions')
def suggestions():
    data = get_json()
    return render_template("trip_suggestions.html", data=data)
