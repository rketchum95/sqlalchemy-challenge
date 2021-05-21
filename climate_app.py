#import dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import numpy as np
import pandas as pd
import datetime as dt
from flask import Flask,jsonify

#Connect to sql database:

engine = create_engine("sqlite:///Resources/hawaii.sqlite",connect_args={'check_same_thread': False})
conn = engine.connect()
Base = automap_base()
Base.prepare(engine,reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
Base.classes.keys()

session = Session(engine)

#Date values for lookups:
Last_date = session.query(func.max(Measurement.date)).all()
prior_year_date = dt.date(2017,8,23) - dt.timedelta(days=365)

#Flask setup
app = Flask(__name__)

#Flask routes
@app.route("/")
def home():
    return(f"Welcome to Surfs Up! <br/>"
           f"**********************<br/>"
          f"Available routes: </br>"
          f"/api/v1.0/stations <br/>"
          f"/api/v1.0/precipitation <br/>"
          f"/api/v1.0/temperatures <br/>"
          f"/api/v1.0/<start> <br/>")
          
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.name).all()
    station_data = list(np.ravel(results))
    session.close()
    return jsonify(station_data)

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.station, Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prior_year_date).all()

    session.close()
    annual_prec = []
    for result in results:
        annual_prec_data = {result.date: result.prcp, "Station": result.station}
        annual_prec.append(annual_prec_data)
        
    return jsonify(annual_prec)


@app.route("/api/v1.0/temperatures")
def temperatures():
    active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()
    
    top_station = active_stations[0][0]
    
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == top_station).\
    filter(Measurement.date>prior_year_date).all()
    
    session.close()
    
    tempdata = []
    for result in results:
        temp_data = {result.date: result.tobs}
        tempdata.append(temp_data)
    
    return jsonify(tempdata)



@app.route("/api/v1.0/<start>")



if __name__ == "__main__":
    app.run(debug=True)