# Import the dependencies.
import datetime as dt
import numpy as np 
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session 
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:////Users/JennyBee/Desktop/SQLAlchemy_Challenge/Starter_Code/Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect = True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station 
# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
# Setting a variable for tobs #
prev_twelve_months = '2016-08-23'
#################################################
# Flask Routes
#################################################
@app.route("/")
def intro():
    return (
        f"<p>Climate Analysis API:"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/station"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<date>"
        f"/api/v1.0/<start>/<end>"
        )
# Query a list for Precipitation Analysis #
@app.route("/api/v1.0/precipitation")
def precipitation():
    """ List of all precipitation within the past 12 months"""
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    previous_year = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date > year_ago).all()
    precipitation = dict(previous_year)
    return jsonify (precipitation)
# Query a list for Station Analysis #
@app.route("/api/v1.0/station")
def station():
    stations = session.query(Station.station).all()
    station = list(np.ravel(stations))
    return jsonify (station)
# Query a list for the dates and temperature observations#
@app.route("/api/v1.0/tobs")
def tobs():
    tobs_results = session.query(Measurement.date, Measurement.station, Measurement.tobs).\
        filter(Measurement.date >= prev_twelve_months).all()
    tobs = list(np.ravel(tobs_results))
    return jsonify (tobs)
# Query a list for the start route 
@app.route("/api/v1.0/<date>")
def start_date(date):
    day_temp = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= date).all()
    temp = list(np.ravel(day_temp))
    return jsonify(temp)
# Query a list for the start and end route 
@app.route("/api/v1.0/<start>/<end>")
def start_end_date (start,end):
    start_end_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    results = list(np.ravel(start_end_results))
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)