# Import the dependencies.

from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

app = Flask(__name__)
# Connect to the database
# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Home route 
@app.route("/")
def home():
    return (
        f"<center><h2>Welcome to the Hawaii Climate Analysis Local API!</h2></center>"
        f"<center><h3>Select from one of the available routes:</h3></center>"
        f"<center>/api/v1.0/precipitation</center>"
        f"<center>/api/v1.0/stations</center>"
        f"<center>/api/v1.0/tobs</center>"
        f"<center>/api/v1.0/start/end</center>"
        )
    
 # /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")   
def precip():
   # Return the previous year's precipitation as a json
   # Calculate the date one year from the last date in data set.
    previousYear = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    #PreviousYear
    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= previousYear).all()

    session.close()
    # Dictionary with the date as the key and the precipitation (prcp) as the value
    precipitation = {date: prcp for date, prcp in results} 
    # Convert to a json
    return jsonify(precipitation)
 
#/api/v1.0/stations route   
@app.route("/api/v1.0/stations")   
def stations():
    
    # Show a list of stations   
    # Perform a query to retrieve the names of stations
    results = session.query(Station.station).all()
    session.close()
    
    stationList = list(np.ravel(results))
    
    # Convert to a json and display
    return jsonify(stationList)

#/api/v1.0/tobs route  
@app.route("/api/v1.0/tobs") 
def temperatures():
    
    # Return the previous year temperatures
    # Calculate the date one year from the last date in data set.
    previousYear = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # PreviousYear
    # Perform a query to retrieve the temperatures from the active station from the past year
    results = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.station == 'USC00519281').\
            filter(Measurement.date >= previousYear).all()
  
    session.close()
   
    temperatureList = list(np.ravel(results))
    
    # Return the list of temperatures
    return jsonify(temperatureList)
# /api/v1.0/<start> and /api/v1.0/<start>/<end> routes
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def dateStats(start=None, end=None):
    
    # Select statement
    selection = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    
    if not end:
        
        startDate = dt.datetime.strptime(start, "%m%d%Y")
        
        results = session.query(*selection).filter(Measurement.date >= startDate).all()
        
        session.close()
        
        temperatureList = list(np.ravel(results))
    
        # Return the list of temperatures
        return jsonify(temperatureList)  
    
    else:
        startDate = dt.datetime.strptime(start, "%m%d%Y")
        endDate = dt.datetime.strptime(end, "%m%d%Y")
        
        results = session.query(*selection)\
            .filter(Measurement.date >= startDate)\
            .filter(Measurement.date <= endDate).all()
            
        session.close()
        
        temperatureList = list(np.ravel(results))
    
        # Return the list of temperatures
        return jsonify(temperatureList)    
        
## app lancher 
if __name__=='__main__':
    app.run(debug=True)
    
