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
        f"/api/v1.0/temp/start<br/>"
        f"api/v1.0/temp/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all precipitation"""

    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    annualprecip = session.query(Measurement.date, Measurement.prcp).\
                    filter(Measurement.date >= year_ago).all()
    precip ={date: prcp for date, prcp in annualprecip}
    return jsonify(precip)

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
                   filter(Measurement.date >= year_ago).all()


   temps = list(np.ravel(annual_temps))

   return jsonify(temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(startdate=None, enddate=None):
    """Return TMIN, TMAX, TAVG"""
    
    sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).\
                filter(Measurement.date >= startdate).all()
        temperatures = list(np.ravel(results))
        return jsonify(temperatures)

    results = session.query(*sel).\
                filter(Measurement.date >= startdate).\
                filter(Measurment.date <= enddate).all()
    temperatures = list(np.ravel(results))
    return jsonify(temerpatures)

if __name__ == "__main__":
    app.run(debug=True)