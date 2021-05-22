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
last_date = session.query(func.max(Measurement.date)).all()
last_date = list(np.ravel(last_date))[0]
last_date=dt.datetime.strptime(last_date,'%Y-%m-%d')
last_year=int(dt.datetime.strftime(last_date,'%Y'))
last_month=int(dt.datetime.strftime(last_date,'%m'))
last_day=int(dt.datetime.strftime(last_date,'%d'))

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
          f"/api/v1.0/startdatesearch/<StartDate> <br/>"
           f"/api/v1.0/daterangesearch/<StartDate>/<EndDate> <br/>"
          f"*    Available dates: 2010-01-01 to 2017-08-23<br/>"
          f"*    For date searches, enter date in format: yyyy-mm-dd")
          
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

@app.route("/api/v1.0/startdatesearch/<StartDate>")
def date1(StartDate):
    sel = [Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)] 
    results = session.query(*sel)\
        .filter(Measurement.date>=StartDate)\
        .group_by(Measurement.date).all()
    
    search_dates=[]
    
    for result in results:
        start_dict = {}
        start_dict["Date"] = result[0]
        start_dict["Low Temp"] = result[1]
        start_dict["High Temp"] = result[2]
        start_dict["Ave Temp"] = result[3]
        search_dates.append(start_dict)
    return jsonify(search_dates)  

@app.route("/api/v1.0/daterangesearch/<StartDate>/<EndDate>")
def date2(StartDate,EndDate):
    sel = [Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)] 
    results = session.query(*sel)\
        .filter(Measurement.date>=StartDate)\
        .filter(Measurement.date<=EndDate)\
        .group_by(Measurement.date).all()
    
    search_dates=[]
    
    for result in results:
        start_dict = {}
        start_dict["Date"] = result[0]
        start_dict["Low Temp"] = result[1]
        start_dict["High Temp"] = result[2]
        start_dict["Ave Temp"] = result[3]
        search_dates.append(start_dict)
    return jsonify(search_dates)        


if __name__ == "__main__":
    app.run(debug=True)