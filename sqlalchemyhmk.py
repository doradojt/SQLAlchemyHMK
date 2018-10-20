import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#Database setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement

Station = Base.classes.station

session = Session(engine)


app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/end/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all precipitation"""

    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    annualprecip = session.query(Measurement.date, Measurement.prcp).\
                    filter(Measurement.date >= year_ago).\
                    order_by(Measurement.date).all()

    return jsonify(annualprecip)

@app.route("/api/v1.0/stations")
def stations():
    """Returns a list of all stations"""
    results = session.query(Station.station).all()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
   """Returns a list of the dates and temperature observations from a year from last data point"""
   year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

   annual_temps = session.query(Measurement.tobs).\
                   filter(Measurement.station == 'USC00519281').\
                   filter(Measurement.date > year_ago).all()


   temps = list(np.ravel(annual_temps))


   return jsonify(temps)

@app.route("/api/v1.0/<start>")
def calc_temps(start_date, end_date):
    answer = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    return jsonify(answer)


if __name__ == "__main__":
    app.run(debug=True)