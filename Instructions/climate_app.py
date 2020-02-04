import numpy as np
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

path = 'Resources/hawaii.sqlite'
engine = create_engine(f"sqlite:///{path}")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return ("Welcome to the Climate App home page!<br/><br/>"
            "These are all the available routes<br/>"
            "/api/v1.0/precipitation<br/>"
            "/api/v1.0/stations<br/>"
            "/api/v1.0/temperature<br/>"
            "/api/v1.0/<startdate>   Kindly enter start date after separator in format YEAR-MONTH-DATE <br/>" 
            "/api/v1.0/<startdate>/<enddate>   Kindly enter start date after 1st separator & end date after \
                2nd separator in format YEAR-MONTH-DATE"
)

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date 1 year ago from the last data point in the database
    start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
    prcp_scores = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= start_date).all() 

    prcp_list = []
    for date, prcp in prcp_scores:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def station():
    station = session.query(Station.station, Station.name)
    station_list = []
    for station, name in station:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_list.append(station_dict)
    
    return jsonify(station_list)

@app.route('/api/v1.0/temperature')
def temperature():
    start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    temp_12_M = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date >= start_date).all()
    temp_list = []
    for date, tobs in temp_12_M:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        temp_list.append(temp_dict)
    return jsonify(temp_list)

@app.route('/api/v1.0/<startdate>')
def calc_temps(startdate):
    describe = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(func.strftime("%Y-%m-%d", Measurement.date) >= startdate).all()
    describe_list = []
    for value in describe:
        describe_dict = {}
        describe_dict["min"] = value[0]
        describe_dict["avg"] = value[1]
        describe_dict["max"] = value[2]
        describe_list.append(describe_dict)
    
    return jsonify(describe_list)

@app.route('/api/v1.0/<startdate>/<enddate>')
def calc_temps_start_end(startdate, enddate):
    describe = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(func.strftime("%Y-%m-%d", Measurement.date) >= startdate).\
                filter(func.strftime("%Y-%m-%d", Measurement.date) <= enddate).all()
    describe_list = []
    for value in describe:
        describe_dict = {}
        describe_dict["min"] = value[0]
        describe_dict["avg"] = value[1]
        describe_dict["max"] = value[2]
        describe_list.append(describe_dict)
    
    return jsonify(describe_list)

if __name__ == "__main__":
    app.run(debug=True)
