from flask import Flask , render_template
import pandas as pd
import numpy as np


app = Flask(__name__)
# Read selected columns from the station names using pandas
stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[["STAID","STANAME                                 "]][:92]

# used decorator and executing home.html and passing station names as HTML data
@app.route("/")
def home():
    return render_template("home.html", data= stations.to_html())

# used decorator user will pass in station, data and extract temperature based on the data in JSON format
@app.route("/api/v1/<station>/<date>")
def about(station,date):
# passing the station number and using zfill,
# we are converting station number to a 6 digit format to match file name
    filename="data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
# using numpy, we are cleaning the unavailable temperature data to NAN
    df["TG"]= df['   TG'].mask(df['   TG'] == -9999, np.nan)
# Extracting temperature from the datasets with pandas
    temperature = df.loc[df['    DATE'] == date]["TG"].squeeze() / 10
    return { "station" : station,
             "date" : date,
             "temperature" : temperature
    }

if __name__ == "__main__":
    app.run(debug=True)