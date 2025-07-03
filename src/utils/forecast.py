import pandas as pd


df_init = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSgwB47qVFZcr1Aq--UWxZ6fDi9CGLZm-1i8QoMgfdaHUbV8EqSli3ayPxYYxD8kqfYYHD41uuNxbjZ/pub?gid=1952392108&single=true&output=csv")
print(df_init.head(-5))


time_column = 'Datetime'
col_target = 'consumption'


print(f"Последняя известная дата - {df_init[time_column].iloc[-1]}")


forecast_horizon_time = '2018-01-03 23:45:00'


import requests


# base_url = "https://nikitasavvin2000-horizon-api-921e.twc1.net"
base_url = "http://0.0.0.0:7079"

def func_generate_forecast(df: pd.DataFrame, time_column: str, col_target: str, forecast_horizon_time: str):
    url = f"{base_url}/forecast"

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




predict_dict = func_generate_forecast(
    df=df_init,
    time_column=time_column,
    col_target=col_target,
    forecast_horizon_time=forecast_horizon_time
)


predictions= predict_dict["predictions"]
df_predictions = pd.DataFrame(predictions)
df_predictions = df_predictions.iloc[1:]

print(df_predictions)

