from flask import Flask, jsonify
from numpy import np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///sqlalchemy-challenge/Resources/hawaii.sqlite")
inspector = inspect(engine)
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
        "/api/v1.0/<start><br>"
        "/api/v1.0/<start>/<end><br>"
    )
@app.route("/api/v1.0/precipitation")
def precip():
    precipitation = session.query(Measurement.date, Measurement.prcp).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    station = session.query(Station.station).all()
    stations = list(np.ravel(station))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    temp = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519281").all()
    temps = list(np.ravel(temp))
    return jsonify(temps)

if __name__ == "__main__":
    app.run(debug=True)    
    
@app.route("/api/v1.0/<start>")
def just_start():
    
@app.route("/api/v1.0/<start>/<end>")
def start_end    