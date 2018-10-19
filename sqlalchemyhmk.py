import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#Database setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement

Station = Base.classes.station

session = Session(engine)


app = Flask(__name__)

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all precipitation"""
    results = session.query(Measurement.date, Measurement.tobs).all()
    
    all_dates_tobs = list(np.ravel(results))

    return jsonify(all_dates_tobs)



@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )



if __name__ == "__main__":
    app.run(debug=True)