import streamlit as st
import requests
import pandas as pd


# Api_key
api_key = "3986444df517b61fd9c0b7ec2ea4561c"


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


    # Benutzerdefinierter Zeitraum
    if weather_type == "Benutzerdefinierter Zeitraum" and city:
        st.write("### Wettervorhersage für den benutzerdefinierten Zeitraum")

        # Kalenderfunktion: Datumseingabe für Start- und Enddatum
        start_date = st.date_input("Startdatum", value=pd.to_datetime("today").date())
        end_date = st.date_input("Enddatum", value=pd.to_datetime("today").date())

        # Button zum Starten
        if st.button("Daten abrufen"):
            if start_date > end_date:
                st.error("Das Startdatum darf nicht nach dem Enddatum liegen.")
            else:
                dates = pd.date_range(start=start_date, end=end_date).date.tolist()

                forecast_16d_data = fetch_16d_forecast(city)
                if forecast_16d_data:
                    st.write(f"Wettervorhersage für die nächsten 16 Tage in {city}:")

                    forecast_16d_df = pd.DataFrame(
                        columns=["Datum", "Temperatur", "Luftfeuchtigkeit", "Beschreibung", "Windgeschwindigkeit"]
                    )

                    temp_list, humidity_list, wind_list, description_list, date_list = [], [], [], [], []

                    for day in forecast_16d_data['list']:
                        # Konvertiert das Datum der API zu einem pandas Timestamp und dann zu einem datetime.date
                        date = pd.to_datetime(day['dt'], unit='s').date()

                        # Vergleiche die Datumseinträge
                        if start_date <= date <= end_date:
                            temp = day['temp']['day']
                            humidity = day['humidity']
                            description = day['weather'][0]['description']
                            wind_speed = day['speed']

                            # Datum und Wetterdaten speichern
                            date_list.append(date)
                            temp_list.append(temp)
                            humidity_list.append(humidity)
                            wind_list.append(wind_speed)
                            description_list.append(description)

                            new_row = pd.DataFrame({
                                "Datum": [date],
                                "Temperatur": [f"{temp}°C"],
                                "Luftfeuchtigkeit": [f"{humidity}%"],
                                "Beschreibung": [description],
                                "Windgeschwindigkeit": [f"{wind_speed} m/s"]
                            })

                            forecast_16d_df = pd.concat([forecast_16d_df, new_row], ignore_index=True)

                    # Speichere die Daten in session_state, damit sie nach der Aktualisierung erhalten bleiben
                    st.session_state.forecast_16d_df = forecast_16d_df
                    st.session_state.date_list = date_list
                    st.session_state.temp_list = temp_list
                    st.session_state.humidity_list = humidity_list
                    st.session_state.wind_list = wind_list

                else:
                    st.error("Es konnten keine Daten abgerufen werden.")
                st.dataframe(forecast_16d_df)

            # Überprüfen, ob die Daten bereits im session_state gespeichert sind
            if 'forecast_16d_df' in st.session_state:
                forecast_16d_df = st.session_state.forecast_16d_df
                date_list = st.session_state.date_list
                temp_list = st.session_state.temp_list
                humidity_list = st.session_state.humidity_list
                wind_list = st.session_state.wind_list

                # Diagramme anzeigen
                chart_type3 = st.selectbox("Wählen Sie eine Rubrik:",
                                           ["Temperatur in Celsius", "Luftfeuchtigkeit in %", "Windgeschwindigkeit in m/s"])

                if chart_type3 == "Temperatur in Celsius":
                    st.line_chart(pd.DataFrame({"Datum": date_list, "Temperatur": temp_list}).set_index("Datum"))
                elif chart_type3 == "Luftfeuchtigkeit in %":
                    st.bar_chart(pd.DataFrame({"Datum": date_list, "Luftfeuchtigkeit": humidity_list}).set_index("Datum"))
                elif chart_type3 == "Windgeschwindigkeit in m/s":
                    st.area_chart(pd.DataFrame({"Datum": date_list, "Windgeschwindigkeit": wind_list}).set_index("Datum"))