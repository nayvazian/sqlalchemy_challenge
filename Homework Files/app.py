import numpy as np
import pandas as pd
import datetime as dt
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station


# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    return (
        f"Welcome to my climate data analysis<br/>"
        f"Here are the links to different analyses<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"For the following two links you manually enter the start and/or end dates into the url<br/>"
        f"Please format the date in yyyy-mm-dd notation.<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"   
    )

# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    prcp_data = []
    for date, precip in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = precip
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)
    
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(station.station).all()

    session.close()

    station_data = []
    for station_name in results:
        station_dict = {}
        station_dict["station"] = station_name
        station_data.append(station_dict)

    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = engine.execute("SELECT tobs, date FROM measurement WHERE station = 'USC00519281' AND date BETWEEN '2016-08-23' AND '2017-08-23'").fetchall()
    session.close()

    temp_data = []
    for date, temp in results:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = temp
        temp_data.append(temp_dict)

    return jsonify(temp_data)


@app.route("/api/v1.0/<start_date>")
def temp_to_present(start_date):
    date = f"'{start_date}'"
    session = Session(engine)
    minimum = engine.execute("SELECT MIN(tobs) FROM measurement WHERE date BETWEEN " + date + " AND '2017-08-23'").fetchall()
    maximum = engine.execute("SELECT MAX(tobs) FROM measurement WHERE date BETWEEN " + date + " AND '2017-08-23'").fetchall()
    mean = engine.execute("SELECT AVG(tobs) FROM measurement WHERE date BETWEEN " + date + " AND '2017-08-23'").fetchall()

    
    session.close()
    
    return jsonify([{"maximum temp" : maximum[0][0], "minimum temp" : minimum[0][0],"mean temp" : mean[0][0]}])

@app.route("/api/v1.0/<start_date>/<end_date>")
def temp_to_date(start_date, end_date):
    date1 = f"'{start_date}'"
    date2 = f"'{end_date}'"
    session = Session(engine)
    minimum = engine.execute("SELECT MIN(tobs) FROM measurement WHERE date BETWEEN " + date1 + " AND " + date2).fetchall()
    maximum = engine.execute("SELECT MAX(tobs) FROM measurement WHERE date BETWEEN " + date1 + " AND " + date2).fetchall()
    mean = engine.execute("SELECT AVG(tobs) FROM measurement WHERE date BETWEEN " + date1 + " AND " + date2).fetchall()

    
    session.close()
    
    return jsonify([{"maximum temp" : maximum[0][0], "minimum temp" : minimum[0][0],"mean temp" : mean[0][0]}])
    
    
if __name__ == "__main__":
    app.run(debug=True)
