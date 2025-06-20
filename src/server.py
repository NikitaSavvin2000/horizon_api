import uvicorn
import pandas as pd
import os

from typing import Annotated, List
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware

from src.config import logger, public_or_local

from src.models.schemes import PredictRequest
import requests

from dotenv import load_dotenv
import os

home_path = os.getcwd()


example_df = pd.read_csv(f'{home_path}/src/examples/example_data.csv')
example_df_short = example_df[:10]
example_df_long = example_df[:1000]
example_df_long = example_df_long.drop(columns="Unnamed: 0")

example_df_json_short = example_df_short.to_dict(orient="records")
example_df_json_long = example_df_long.to_dict(orient="records")


load_dotenv()
base_url = os.getenv("FORECAST_ENDPOINT")

if public_or_local == 'LOCAL':
    url = 'http://localhost'
else:
    url = 'http://77.37.136.11'

origins = [
    url
]
docs_url = "/horizon_api"
app = FastAPI(docs_url=docs_url, openapi_url='/backend/v1/openapi.json')
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/forecast")
async def func_generate_forecast(body: Annotated[
    PredictRequest, Body(
        example={
            "df": example_df_json_long,
            "time_column": "time",
            "col_target": "load_consumption",
            "forecast_horizon_time": "2022-09-10 05:55:00"
        })]):

    """
    Generates a time series forecast based on historical data.

    Description:
    ------------
    The function takes a time series, normalizes the data, forms a future time interval, and performs forecasting.
    It returns the result in JSON format, which includes the latest known data and forecasted values
    for frontend visualization.

    Parameters:
    -----------
    1. `df` (json) — The input DataFrame containing the time series with the target variable.
    2. `time_column` (str) — The name of the column containing timestamps.
    3. `col_target` (str) — The name of the target variable for forecasting.
    4. `forecast_horizon_time` (str) — The forecast horizon (last possible forecast datetime).

    Returns:
    --------
    1. predictions — the forecasted data

    Example API call in Python:

    ------------------
    ```
    import requests
    import pandas as pd

    def func_generate_forecast(df: pd.DataFrame, time_column: str, col_target: str, forecast_horizon_time: str):
        url = "http://your_backend_url/backend/v1/generate_forecast"

        df_records = df.to_dict(orient='records')

        data = {
            "df": df_records,
            "time_column": time_column,
            "col_target": col_target,
            "forecast_horizon_time": forecast_horizon_time
        }

        try:
            response = requests.post(url, json=data)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка при запросе: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            return None

    df = pd.read_csv(<here yor data>)

    time_column = 'time'
    col_target = 'load_consumption'
    forecast_horizon_time = '2022-09-10 05:00:00'
    df[time_column] = pd.to_datetime(df[time_column])

    response = func_generate_forecast(df, time_column, col_target, forecast_horizon_time)
    ```
    """

    try:
        json_df = body.df
        time_column = body.time_column
        col_target = body.col_target
        forecast_horizon_time = body.forecast_horizon_time

        data = {
            "df": json_df,
            "time_column": time_column,
            "col_target": col_target,
            "forecast_horizon_time": forecast_horizon_time
        }
        url = f"{base_url}/generate_forecast"
        print(url)
        response = requests.post(url, json=data)
        response.raise_for_status()
        res = response.json()
        predictions = res["map_data"]["data"]["predictions"]

        return {"predictions": predictions}

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"Error: {str(e)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unknown error",
            headers={"X-Error": f"{repr(e)}"},
        )
@app.get("/")
def read_root():
    return {"message": "Welcome to the Horizon System API"}



if __name__ == "__main__":
    port = 7079
    print(f'🚀 Документация http://0.0.0.0:{port}{docs_url}')
    uvicorn.run("server:app", host="0.0.0.0", port=port, workers=2, log_level="debug")

