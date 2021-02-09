import os
import sys
import argparse
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

from azureml.studio.core.io.data_frame_directory import load_data_frame_from_directory, save_data_frame_to_directory

from fbprophet import Prophet
from fbprophet.plot import add_changepoints_to_plot
from matplotlib import pyplot
import pickle
from azureml.core.run import Run
import logging



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

# Get context
run = Run.get_context()

##Create the Forecast plot
fig = model.plot(forecast)
a = add_changepoints_to_plot(fig.gca(), model, forecast)
run.log_image("Forecast", plot=fig)
pyplot.savefig(args.Model_Path + "/" +'forecast.png')

##Create the components plots
fig2 = model.plot_components(forecast)
run.log_image("Forecast Components", plot=fig2)
pyplot.savefig(args.Model_Path + "/" +'components.png')

##Print prediction
model_output = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(args.periods).copy()
model_output['Date']=model_output['ds'].dt.strftime('%Y-%m-%d')
model_output = model_output.drop('ds', axis=1)
model_output = model_output[ ['Date'] + [ col for col in model_output.columns if col != 'Date' ] ]
model_output.to_csv(args.Model_Path +"/"+ args.Model_FileName + '.csv')
forecast_show = model_output.tail(10)

def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')
    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in mpl_table._cells.items():
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    return ax.get_figure(), ax

fig,ax = render_mpl_table(forecast_show, header_columns=0, col_width=3.0)
run.log_image("Forecast Components", plot=fig)
fig.savefig(args.Model_Path + "/""table_mpl.png")

#run.log_image(name = 'Forecast', plot=html_forecast)

#Save model
with open(args.Model_Path +"/"+ args.Model_FileName + '.pkl', 'wb') as handle:
    pickle.dump(model, handle, protocol=pickle.HIGHEST_PROTOCOL)

## Output model
save_data_frame_to_directory(args.Evaluation_Output, model_output)
