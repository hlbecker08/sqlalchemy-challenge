# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date one year from the last date in data set.
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365) 


    # Perform a query to retrieve the data and precipitation scores
    data_prcp = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= one_year_ago).all()
    

    # Save the query results as a Pandas DataFrame. Explicitly set the column names
    df = pd.DataFrame(data_prcp, columns=['Date', 'Precipitation'])

    # Sort the dataframe by date
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    session.close()

@app.route("/api/v1.0/stations")
def stations():
    session.query(station.station).all()
    session.close()
@app.route("/api/v1.0/tobs")
def tobs():
    # Calculate the date one year from the last date in data set.
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365) 

    # Query the last 12 months of temperature observation data for station USC00519281
    data_temp = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date >= one_year_ago).\
    filter(measurement.station == 'USC00519281').all()
    session.close()
