import requests
import pandas as pd
import plotly.graph_objects as go

base_url = "http://0.0.0.0:7078/backend/v1"

def func_generate_forecast(df: pd.DataFrame, time_column: str, col_target: str, forecast_horizon_time: str):
    url = f"{base_url}/generate_forecast"

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

df_data = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSgwB47qVFZcr1Aq--UWxZ6fDi9CGLZm-1i8QoMgfdaHUbV8EqSli3ayPxYYxD8kqfYYHD41uuNxbjZ/pub?gid=1952392108&single=true&output=csv")

time_column = 'Datetime'
col_target = 'consumption'

forecast_horizon_time = '2018-01-07 23:45:00 '

predict_dict = func_generate_forecast(
    df=df_data,
    time_column=time_column,
    col_target=col_target,
    forecast_horizon_time=forecast_horizon_time
)

predictions= predict_dict["map_data"]["data"]["predictions"]
df_predictions = pd.DataFrame(predictions)
df_predictions = df_predictions.iloc[1:]

print(df_predictions)

fig = go.Figure()

fig.add_trace(go.Scatter(
    y=y_pred,
    mode='lines',
    name='Forecast',
    line=dict(color='orange')
))

fig.show()