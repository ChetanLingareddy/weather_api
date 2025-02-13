from flask import Flask, render_template
import pandas as pd
import numpy as np

app = Flask ( __name__ )

# Load station names from the dataset (first 92 entries)
stations = pd.read_csv ( "data_small/stations.txt", skiprows=17 )
stations = stations[["STAID", "STANAME                                 "]][:92]


@app.route ( "/" )
def home() :
    """Render the home page with station data."""
    return render_template ( "home.html", data=stations.to_html () )

# code For a particular station on a particular date
@app.route ( "/api/v1/<station>/<date>" )
def get_temperature(station, date) :
    """Fetch and return temperature data for a given station and date."""

    # Format station number to match the filename convention with .zfill
    filename = f"data_small/TG_STAID{str ( station ).zfill ( 6 )}.txt"
    df = pd.read_csv ( filename, skiprows=20, parse_dates=["    DATE"] )

    # Replace missing temperature values (-9999) with NaN
    df["TG"] = df["   TG"].replace ( -9999, np.nan )

    # Extract temperature for the given date
    temperature = df.loc[df["    DATE"] == date]["TG"].squeeze () / 10
    return {
        "station" : station,
        "date" : date,
        "temperature" : temperature
    }

# Code For a particular station in all dates.
@app.route( "/api/v1/<station>")
def only_station(station):
    filename = f"data_small/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    # Converting data frame to dictionary.
    result = df.to_dict(orient="records")
    return result

# Code For a particular station on a particular year
@app.route( "/api/v1/yearly/<station>/<year>")
def data(station,year):
    filename = f"data_small/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20)
    # converting date variable data to string
    df["    DATE"]=df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))]
    result = result.to_dict ( orient="records" )
    return result


if __name__ == "__main__" :
    app.run ( debug=True )
