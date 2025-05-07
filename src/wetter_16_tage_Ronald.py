import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")



#Funktion für 16 Tage-Vorhersagen
def fetch_16d_forecast(city):
    forecast_16d_url = "http://api.openweathermap.org/data/2.5/forecast/daily"
    params = {
        "q": city,
        "cnt": 16,   # Anzahl der Tage
        "appid": api_key,
        "units":"metric",
        "lang":"de"
    }
    response = requests.get(forecast_16d_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Fehler beim Abrufen der 16-Tages-Vorhersage")
        return None



# Streamlit Main Page
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

    weather_type = st.radio("Triff eine Auswahl",
                            ("Aktuelles Wetter",
                             "3 Stundenintervall Heute",
                             "Wettervorhersage für die nächsten 5 Tage",
                             "Wettervorhersage für die nächsten 16 Tage",
                             "Benutzerdefinierter Zeitraum")
                            )

    city = st.text_input("Gib eine Stadt ein", "Berlin")

    if weather_type == "Wettervorhersage für die nächsten 16 Tage" and city:
            forecast_16d_data = fetch_16d_forecast(city)
            if forecast_16d_data:
                st.write(f"Wettervorhersage für die nächsten 16 Tage in {city}:")

                forecast_16d_df = pd.DataFrame(
                    columns=["Datum",
                            "Temperatur",
                            "Luftfeuchtigkeit",
                            "Beschreibung",
                            "Windgeschwindigkeit"]
                )

                temp_list, humidity_list, wind_list, date_list = [], [], [], []

                for day in forecast_16d_data['list']:
                    date = pd.to_datetime(day['dt'], unit='s').strftime('%Y-%m-%d')
                    temp = day['temp']['day']
                    humidity = day['humidity']
                    description = day['weather'][0]['description']
                    wind_speed = day['speed']

                    # Datum und Wetterdaten speichern
                    date_list.append(date)
                    temp_list.append(temp)
                    humidity_list.append(humidity)
                    wind_list.append(wind_speed)

                    new_row = pd.DataFrame({
                        "Datum": [date],
                        "Temperatur": [f"{temp}°C"],
                        "Luftfeuchtigkeit": [f"{humidity}%"],
                        "Beschreibung": [description],
                        "Windgeschwindigkeit": [f"{wind_speed} m/s"]
                    })

                    forecast_16d_df = pd.concat([forecast_16d_df, new_row], ignore_index=True)

                # Diagramme
                chart_type2 = st.selectbox("Wählen Sie eine Rubrik:",
                                        ["Temperatur in Celsius", "Luftfeuchtigkeit in %", "Windgeschwindigkeit in m/s"])

                if chart_type2 == "Temperatur in Celsius":
                    st.line_chart(pd.DataFrame({"Datum": date_list, "Temperatur": temp_list}).set_index("Datum"))
                elif chart_type2 == "Luftfeuchtigkeit in %":
                    st.bar_chart(pd.DataFrame({"Datum": date_list, "Luftfeuchtigkeit": humidity_list}).set_index("Datum"))
                elif chart_type2 == "Windgeschwindigkeit in m/s":
                    st.area_chart(pd.DataFrame({"Datum": date_list, "Windgeschwindigkeit": wind_list}).set_index("Datum"))

            st.dataframe(forecast_16d_df)