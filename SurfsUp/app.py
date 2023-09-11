# Import the dependencies.
import numpy as np
import pandas as pd
import markdown

import datetime as dt
from datetime import datetime
from dateutil.relativedelta import relativedelta

from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func




#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# # reflect an existing database into a new model
Base = automap_base()

# # reflect the tables
Base.prepare(autoload_with=engine)

# # Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# # Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Useful vars
#################################################
# Find the most recent date in the data set.
most_recent_date = session.query(func.max(Measurement.date)).first()[0]

# Starting from the most recent data point in the database. 
most_recent_date_date = datetime.strptime(most_recent_date, "%Y-%m-%d").date()

# Calculate the date one year from the last date in data set.
one_year_prior_date = most_recent_date_date - relativedelta(years=1)
one_year_prior = one_year_prior_date.strftime("%Y-%m-%d")


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
# start at the homepage
# list all the available routes
@app.route('/')
def welcome():
    return markdown.markdown('''
# Climate App
## Module 10 Challenge

---

Active routes:

- [Precipitation Measurements All Stations from the last recorded 12 months](/api/v1.0/precipitation): /api/v1.0/precipitation
- [All Stations](/api/v1.0/stations): /api/v1.0/stations
- [Temperature of the Most Active Station](/api/v1.0/tobs): /api/v1.0/tobs
- [Up Til Now](/api/v1.0/2016-08-23): /api/v1.0/**[[YYYY-MM-DD]]**
- [Between Two Dates](/api/v1.0/2016-08-23/2017-08-23): /api/v1.0/**[[YYY-MM-DD]]**/**[[YYY-MM-DD]]**
''')


# - Convert the query results from your precipitation analysis
#   (i.e. retrieve only the last 12 months of data) to a dictionary using date
#   as the key and prcp as the value.
# - Return the JSON representation of your dictionary.
@app.route('/api/v1.0/precipitation')
def precipitation():

    measurements_one_year = session.query(Measurement.date, 
                                          Measurement.prcp)\
                                    .filter(Measurement.date >= one_year_prior)\
                                    .order_by(Measurement.date)\
                                    .all()

    result = []

    for measurement in measurements_one_year:
        d = {}
        d[measurement.date] = measurement.prcp
        result.append(d)

    return jsonify(result)


# - Return a JSON list of stations from the dataset.
@app.route('/api/v1.0/stations')
def stations():
    # stations = session.query(Station.station).all()

    # result = list(np.ravel(stations))

    stations = session.query(Station).all()

    result = []
    for s in stations:
        d = {}
        d["id"] = s.id
        d["station"] = s.station
        d["name"] = s.name
        d["latitude"] = s.latitude
        d["longitude"] = s.longitude
        d["elevation"] = s.elevation
        result.append(d)

    return jsonify(result)


# - Query the dates and temperature observations of the most-active station
#   for the previous year of data.
# - Return a JSON list of temperature observations for the previous year.
@app.route('/api/v1.0/tobs')
def tobs():
    stations_activity = session.query(Measurement.station, func.count(Measurement.station))\
        .group_by(Measurement.station)\
        .order_by(func.count(Measurement.station).desc())\
        .all()

    most_active_station = stations_activity[0][0]

    top_station_one_year = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.date >= one_year_prior)\
        .filter(Measurement.station == most_active_station)\
        .all()

    result = []

    for measurement in top_station_one_year:
        d = {}
        d[measurement.date] = measurement.tobs
        result.append(d)

    return jsonify(result)


# - Return a JSON list of the minimum temperature, the average temperature,
#   and the maximum temperature for a specified start or start-end range.
# - For a specified start, calculate TMIN, TAVG, and TMAX for all the dates
#   greater than or equal to the start date.
@app.route('/api/v1.0/<start>')
def start(start):
    canon_start = start

    measurements_since = session.query(Measurement.date,
                                       func.min(Measurement.tobs),
                                       func.avg(Measurement.tobs),
                                       func.max(Measurement.tobs))\
                                .filter(Measurement.date >= canon_start)\
                                .group_by(Measurement.date)\
                                .all()

    result = []

    for measurement in measurements_since:
        d = {}
        d["Date"] = measurement[0]
        d["TMIN"] = measurement[1]
        d["TAVG"] = measurement[2]
        d["TMAX"] = measurement[3]
        result.append(d)

    return jsonify(result)


# - For a specified start date and end date, calculate TMIN, TAVG, and TMAX
#   for the dates from the start date to the end date, inclusive.
@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end):
    canon_start = start
    canon_end = end

    measurements_between = session.query(Measurement.date,
                                         func.min(Measurement.tobs),
                                         func.avg(Measurement.tobs),
                                         func.max(Measurement.tobs))\
                                  .filter(Measurement.date >= canon_start)\
                                  .filter(Measurement.date <= canon_end)\
                                  .group_by(Measurement.date)\
                                  .all()

    result = []

    for measurement in measurements_between:
        d = {}
        d["Date"] = measurement[0]
        d["TMIN"] = measurement[1]
        d["TAVG"] = measurement[2]
        d["TMAX"] = measurement[3]
        result.append(d)

    return jsonify(result)


session.close()

# Debug
if __name__ == "__main__":
    app.run(debug=True)
