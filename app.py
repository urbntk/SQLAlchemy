import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd

from flask import Flask, jsonify
import datetime as dt
import datetime
from datetime import timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
                       
# We can view all of the classes that automap found
Base.classes.keys()

                       # Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

        
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of dates and precipitation"""
    # Query all passengers
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Convert list of tuples into normal list
    all_prcp = list(np.ravel(results))

    return jsonify(all_prcp)
        
##Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
##Return the JSON representation of your dictionary.



@app.route("/api/v1.0/stations")
#Return a JSON list of stations from the dataset.
        
def stations():
    """Return a JSON list of stations from the dataset"""
    # Query all passengers

    session = Session(engine)
    results = session.query(Measurement.station).group_by(Measurement.station).all()

    station_names = list(np.ravel(results))

    return jsonify(station_names)
        
#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for name, age, sex in results:
#         passenger_dict = {}
#         passenger_dict["name"] = name
#         passenger_dict["age"] = age
#         passenger_dict["sex"] = sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)

@app.route("/api/v1.0/tobs")
def date_and_tobs():
    #`/api/v1.0/tobs`
    #* query for the dates and temperature observations from a year from the last data point.
    #* Return a JSON list of Temperature Observations (tobs) for the previous year.

    """Return a JSON list of stations from the dataset"""
    # Query all passengers

    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).all()


    # Create a dictionary from the row data and append to a list of date and tobs
    all_date_tobs = []
    for date, tobs in results:
        date_tobs_dict = {}
        date_tobs_dict["date"] = date
        date_tobs_dict["tobs"] = tobs
        all_date_tobs.append(date_tobs_dict)


    all_date_tobs_df = pd.DataFrame(all_date_tobs)

    #get last date of the data frame( 2017-08-23)
    Last_date =  max(all_date_tobs_df.date)

    #put the last date of the df into a date formatted object
    Last_date3 = dt.datetime.strptime(Last_date, "%Y-%m-%d").date()

    start_date = Last_date3 + relativedelta(years=-1)


    #query 1 year range for date and tobs
    perecip_scores_1year = session.query(Measurement.date, Measurement.tobs) \
        .filter(Measurement.date <= Last_date3) \
        .filter(Measurement.date >= start_date) \
        .order_by(Measurement.date.desc()).all()

    #cerate a dictionary to put the list values into
    all_date_tobs_1year = []
    for date, tobs in perecip_scores_1year:
        date_tobs_dict_1year = {}
        date_tobs_dict_1year["date"] = date
        date_tobs_dict_1year["tobs"] = tobs
        all_date_tobs_1year.append(date_tobs_dict_1year)

    return jsonify(all_date_tobs_1year)
    #return jsonify(all_date_tobs)


@app.route("/api/v1.0/<start>")
def date_and_tobs_start():
    #`/api/v1.0/tobs`
    #* query for the dates and temperature observations from a year from the last data point.
    #* Return a JSON list of Temperature Observations (tobs) for the previous year.

    """Return a JSON list of stations from the dataset"""
    # Query all passengers

    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).all()


    # Create a dictionary from the row data and append to a list of date and tobs
    all_date_tobs = []
    for date, tobs in results:
        date_tobs_dict = {}
        date_tobs_dict["date"] = date
        date_tobs_dict["tobs"] = tobs
        all_date_tobs.append(date_tobs_dict)


    all_date_tobs_df = pd.DataFrame(all_date_tobs)

    #get last date of the data frame( 2017-08-23)
    Last_date =  max(all_date_tobs_df.date)

    #put the last date of the df into a date formatted object
    Last_date3 = dt.datetime.strptime(Last_date, "%Y-%m-%d").date()

    start_date = Last_date3 + relativedelta(years=-1)


    #query 1 year range for date and tobs
    perecip_scores_1year = session.query(Measurement.date, Measurement.tobs) \
        .filter(Measurement.date <= Last_date3) \
        .filter(Measurement.date >= start_date) \
        .order_by(Measurement.date.desc()).all()

    #cerate a dictionary to put the list values into
    all_date_tobs_1year = []
    for date, tobs in perecip_scores_1year:
        date_tobs_dict_1year = {}
        date_tobs_dict_1year["date"] = date
        date_tobs_dict_1year["tobs"] = tobs
        all_date_tobs_1year.append(date_tobs_dict_1year)

    return jsonify(all_date_tobs_1year)
    #return jsonify(all_date_tobs)





if __name__ == '__main__':
    app.run(debug=True)
