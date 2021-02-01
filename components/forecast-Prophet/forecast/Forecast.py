import os
import sys
import argparse
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import mean_squared_error

from azureml.studio.core.io.data_frame_directory import load_data_frame_from_directory, save_data_frame_to_directory

from fbprophet import Prophet
from fbprophet.plot import add_changepoints_to_plot
from matplotlib import pyplot
import pickle



## Parse args
parser = argparse.ArgumentParser("Forecast")
parser.add_argument("--Training_Data", type=str, help="Training dataset")
parser.add_argument("--Timeseries", type=str, help="Your time series column.")
parser.add_argument("--Forecast_qt", type=str, help="The quantity to be forecast.")
parser.add_argument("--daily_seasonality", type=bool, help="Only True for daily")
parser.add_argument("--periods", type=int, help="Number of forecast periods")
parser.add_argument("--freq", type=str, help="Frequency of Forecast, D for Daily, M for Monthly")
parser.add_argument("--Add_Holidays", type=str, help="Country Holidays, example UK")
#parser.add_argument("--fct_period", type=str, help="Time period of the forecast)
parser.add_argument("--Model_FileName", type=str, help="Name of the model file.")
parser.add_argument("--Model_Path", type=str, help="Path to store the prophet model.")
parser.add_argument("--Evaluation_Output", type=str, help="Evaluation result")
args = parser.parse_args()

## Load data from DataFrameDirectory to Pandas DataFrame
loaded_df = load_data_frame_from_directory(args.Training_Data).data

## Prepare training data

training_df = loaded_df[[args.Timeseries , args.Forecast_qt]].copy()
ts = training_df.rename(columns={args.Timeseries:'ds',args.Forecast_qt:'y'})
ts['ds']= pd.to_datetime(ts['ds'])

## Training
model = Prophet(daily_seasonality = args.daily_seasonality)
#add country holidays
model.add_country_holidays(country_name=args.Add_Holidays)
# fit the model
model.fit(ts)

##Create the container for the forecast
future = model.make_future_dataframe(periods=args.periods, freq=args.freq)

##Run the forecast
forecast = model.predict(future)

#check output dir
os.makedirs(args.Model_Path, exist_ok=True)

##Create the Forecast plot
fig = model.plot(forecast)
a = add_changepoints_to_plot(fig.gca(), model, forecast)
pyplot.savefig(args.Model_Path + "/" +'forecast.png')

##Create the components plots
fig2 = model.plot_components(forecast)
pyplot.savefig(args.Model_Path + "/" +'components.png')

##Print prediction
model_output = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(args.periods)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(args.periods))

#Save model
with open(args.Model_Path +"/"+ args.Model_FileName + '.pkl', 'wb') as handle:
    pickle.dump(model, handle, protocol=pickle.HIGHEST_PROTOCOL)

## Output model
save_data_frame_to_directory(args.Evaluation_Output, model_output)
