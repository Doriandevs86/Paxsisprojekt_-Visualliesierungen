import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Api_key
api_key = "Dein API Key"


# Funktion, um aktuelle Wetterdaten abzurufen
def fetch_current_weather(city):
    current_weather_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "de"
    }

    response = requests.get(current_weather_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Fehler beim Abrufen der aktuellen Wetterdaten")
        return None


# Funktion für stündliche und 5 Tages Vorhersage
def fetch_5d_forecast(city):
    forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "de"
    }
    response = requests.get(forecast_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Fehler beim Abrufen der 4-Stunden-Vorhersage")
        return None




#Streamlitseite
st.title("Praxisprojekt Datenvisualisierung")
st.sidebar.title("Navigation")
st.sidebar.markdown("")
page = st.sidebar.radio(" ",
                        ["Startseite",
                         "Wetterdaten",
                         "Wettervergleich",
                         "Globale Wetterkarte (coming soon)",
                         "Kontakt",
                         "Impressum"]
                        )


#aktuelles Wetter
if page == "Wetterdaten":
    st.header("Wetterdaten")

    weather_type = st.radio("Triff eine Auswahl",
                            ("Aktuelles Wetter",
                             "3 Stundenintervall Heute",
                             "Wettervorhersage für die nächsten 5 Tage",
                             "Wettervorhersage für die nächsten 16 Tage",
                             "Benutzerdefinierter Zeitraum")
                            )

    city = st.text_input("Gib eine Stadt ein", "Berlin")

    # Aktuelles Wetter anzeigen
    if weather_type == "Aktuelles Wetter" and city:
        current_weather_data = fetch_current_weather(city)
        if current_weather_data:
            # Extrahieren der Daten
            city_name = current_weather_data['name']
            temperature = current_weather_data['main']['temp']
            humidity = current_weather_data['main']['humidity']
            description = current_weather_data['weather'][0]['description']
            wind_speed = current_weather_data['wind']['speed']



            st.write(f"Aktuelles Wetter in:")
            st.write(f"**Stadt:** {city_name}")
            st.write(f"**Wetterlage:** {description}")
            st.write(f"**Temperatur:** {temperature} °C")
            st.write(f"**Luftfeuchtigkeit:** {humidity} %")
            st.write(f"**Windgeschwindigkeit:** {wind_speed} m/s")
            st.divider()

            # DataFrame
            current_weather_df = pd.DataFrame({
                "Rubrik": ["Temperatur", "Luftfeuchtigkeit", "Beschreibung", "Windgeschwindigkeit"],
                "Wert": [f"{temperature} °C", f"{humidity} %", description, f"{wind_speed} m/s"]
            })

            st.dataframe(current_weather_df)


    # Wettervorhersage für die nächsten 3 Stunden anzeigen
    if weather_type == "3 Stundenintervall Heute" and city:
        forecast_3h_data = fetch_5d_forecast(city)
        if forecast_3h_data:
            st.write(f"3 Stundenintervall heute in {city}:")

            time_list, temp_list, humidity_list, wind_list = [], [], [], []

            forecast_3h_df = pd.DataFrame(
                columns=["Zeit", "Temperatur", "Luftfeuchtigkeit", "Beschreibung", "Windgeschwindigkeit"]
            )

            today = datetime.now().date()

            for item in forecast_3h_data['list']:
                dt = datetime.fromtimestamp(item['dt'])
                if dt.date() == today:
                    time_only = dt.strftime('%H:%M')
                    temp = item['main']['temp']
                    humidity = item['main']['humidity']
                    description = item['weather'][0]['description']
                    wind_speed = item['wind']['speed']

                    # Daten speichern
                    time_list.append(time_only)
                    temp_list.append(temp)
                    humidity_list.append(humidity)
                    wind_list.append(wind_speed)

                    # Dataframe
                    new_row = pd.DataFrame({
                        "Zeit": [time_only],
                        "Temperatur": [f"{temp}°C"],
                        "Luftfeuchtigkeit": [f"{humidity}%"],
                        "Beschreibung": [description],
                        "Windgeschwindigkeit": [f"{wind_speed} m/s"]
                    })
                    forecast_3h_df = pd.concat([forecast_3h_df, new_row], ignore_index=True)
            # Diagramme
            chart_type = st.selectbox("Wählen Sie eine Rubrik:",
                                    ["Temperatur in Celsius", "Luftfeuchtigkeit in %",
                                    "Windgeschwindigkeit in m/s"])

            if chart_type == "Temperatur in Celsius":
                st.line_chart(pd.DataFrame({"Zeit": time_list, "Temperatur": temp_list}).set_index("Zeit"))
            elif chart_type == "Luftfeuchtigkeit in %":
                st.bar_chart(
                    pd.DataFrame({"Zeit": time_list, "Luftfeuchtigkeit": humidity_list}).set_index("Zeit"))
            elif chart_type == "Windgeschwindigkeit in m/s":
                st.area_chart(
                    pd.DataFrame({"Zeit": time_list, "Windgeschwindigkeit": wind_list}).set_index("Zeit"))

                st.dataframe(forecast_3h_df)
