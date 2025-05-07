import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")


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



# Streamlitseite
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


if page == "Wetterdaten":
    st.header("Wetterdaten")

    city = st.text_input("Gib eine Stadt ein", "Berlin")
    weather_type = st.radio("Triff eine Auswahl",
                            ("Aktuelles Wetter",
                             "3 Stundenintervall Heute",
                             "Wettervorhersage für die nächsten 5 Tage",
                             "Wettervorhersage für die nächsten 16 Tage",
                             "Benutzerdefinierter Zeitraum")
                            )

    # Wettervorhersage für die nächsten 5 Tage
    if  weather_type == "Wettervorhersage für die nächsten 5 Tage" and city:
        forecast_5d_data = fetch_5d_forecast(city)
        if forecast_5d_data and city:

            st.write(f"Wettervorhersage für die nächsten 5 Tage in {city}:")

            forecast_list = []

            for day in forecast_5d_data['list']:
                date = pd.to_datetime(day['dt'], unit='s').strftime('%Y-%m-%d')
                temp = day['main']['temp']
                humidity = day['main']['humidity']
                wind_speed = day['wind']['speed']

                forecast_list.append({
                    "Datum": date,
                    "Temperatur": temp,
                    "Luftfeuchtigkeit": humidity,
                    "Windgeschwindigkeit": wind_speed
                })

            # Erstellen des DataFrames
            forecast_df = pd.DataFrame(forecast_list)

            # Gruppierung nach Datum
            grouped_df = forecast_df.groupby('Datum').agg({
                "Temperatur": "mean",
                "Luftfeuchtigkeit": "mean",
                "Windgeschwindigkeit": "mean"
            }).reset_index()



            # Auswahl für den Plot
            chart_type1 = st.selectbox("Wählen Sie eine Rubrik:",
                                    ["Temperatur in Celsius", "Luftfeuchtigkeit in %", "Windgeschwindigkeit in m/s"])

            # Diagramme
            if chart_type1 == "Temperatur in Celsius":
                st.line_chart(grouped_df.set_index('Datum')[['Temperatur']])

            elif chart_type1 == "Luftfeuchtigkeit in %":
                st.bar_chart(grouped_df.set_index('Datum')[['Luftfeuchtigkeit']])

            elif chart_type1 == "Windgeschwindigkeit in m/s":
                st.area_chart(grouped_df.set_index('Datum')[['Windgeschwindigkeit']])

            st.dataframe(grouped_df)