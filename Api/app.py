from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

#Flask Setup
app = Flask(__name__)

#Flask Routes

@app.route("/")
def welcome():
    return (
        "Welcome to Home Page!<br>"
        "Available Routes:<br>"
        "/api/v1.0/precipitation<br>"
        "/api/v1.0/stations<br>"
        "/api/v1.0/tobs<br>"
        "/api/v1.0/start<br>"
        "/api/v1.0/start/end"
    )
@app.route("/api/v1.0/precipitation")
def precip():
    precipitation = session.query(Measurement.date, Measurement.prcp).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()
    stations_list = list(np.ravel(stations))
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    temp = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519281").all()
    temps = list(np.ravel(temp))
    return jsonify(temps)
     
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_end(start = None, end = None):
    values = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    if not end:
        results = session.query(*values).filter(Measurement.date >= start).all()
        start_temp = list(np.ravel(results))
        return jsonify(start_temp)
    
    
    results = session.query(*values).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    start_temp = list(np.ravel(results))
    return jsonify(start_temp)

if __name__ == "__main__":
    app.run(debug=True)   