import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import matplotlib as plt

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


# Wettervergleichsseite
if page == "Wettervergleich":
    city = st.text_input("Stadt eingeben", "Berlin")

    start_date = st.date_input("Startdatum", value=pd.to_datetime("today").date())
    end_date = st.date_input("Enddatum", value=pd.to_datetime("today").date())


    if st.button("Daten abrufen und vergleichen"):
        forecast_data = fetch_16d_forecast(city)

        if forecast_data:
            # Daten extrahieren
            all_dates = [datetime.fromtimestamp(day['dt']).date() for day in forecast_data['list']]

            # Indizes für den gewählten Zeitraum finden
            start_idx = next((i for i, d in enumerate(all_dates) if d >= start_date), None)
            end_idx = next((i for i, d in enumerate(all_dates) if d >= end_date), None)

            st.divider()

            # Prüfen, ob die Daten im Zeitraum vorhanden sind
            if start_idx is not None and end_idx is not None:
                dates = all_dates[start_idx:end_idx + 1]
                temp_list = [forecast_data['list'][i]['temp']['day'] for i in range(start_idx, end_idx + 1)]
                humidity_list = [forecast_data['list'][i]['humidity'] for i in range(start_idx, end_idx + 1)]
                wind_list = [forecast_data['list'][i]['speed'] for i in range(start_idx, end_idx + 1)]

                # Auswahl des Diagrammtyps
                st.write(f"### Wetterentwicklung in {city} von {start_date} bis {end_date}")
                chart_type = st.selectbox("Wählen Sie eine Rubrik:",
                                            ["Temperatur in Celsius",
                                            "Luftfeuchtigkeit in %",
                                            "Windgeschwindigkeit in m/s"]
                                            )

                if chart_type == "Temperatur in Celsius":
                    st.line_chart(pd.DataFrame({"Datum": dates, "Temperatur": temp_list}).set_index("Datum"))
                elif chart_type == "Luftfeuchtigkeit in %":
                    st.bar_chart(pd.DataFrame({"Datum": dates, "Luftfeuchtigkeit": humidity_list}).set_index("Datum"))
                elif chart_type == "Windgeschwindigkeit in m/s":
                    st.area_chart(pd.DataFrame({"Datum": dates, "Windgeschwindigkeit": wind_list}).set_index("Datum"))
                today = datetime.now().date()

                # Vergleich zwischen Start- und Enddatum
                start_data = forecast_data['list'][start_idx]
                end_data = forecast_data['list'][end_idx]

                vergleichs_df = pd.DataFrame({
                    "Parameter": ["Temperatur (°C)",
                                    "Luftfeuchtigkeit (%)",
                                    "Windgeschwindigkeit (m/s)"],

                    f"{start_date}": [
                        start_data['temp']['day'],
                        start_data['humidity'],
                        start_data['speed']
                    ],
                    f"{end_date}": [
                        end_data['temp']['day'],
                        end_data['humidity'],
                        end_data['speed']
                    ]
                })

                st.divider()


                plt.style.use("dark_background")
                st.write(f"### Vergleichsdiagramm des Wetters in {city} zwischen {start_date} und {end_date}")
                st.dataframe(vergleichs_df)

                # Vergleichs-Diagram
                st.write("### Vergleichsdiagramm")

                ax = vergleichs_df.set_index("Parameter").plot(kind="bar", color=['#1f77b4', '#ff7f0e'])

                ax.set_title(f"Wettervergleich in {city} zwischen {start_date} und {end_date}", color='white')

                ax.set_xlabel("Parameter", color='white')
                ax.tick_params(axis='x', colors='white', rotation=45)
                ax.tick_params(axis='y', colors='white')
                ax.set_facecolor('#2c2f38')

                # Diagramm anzeigen
                st.pyplot(plt.gcf())
                plt.clf()


            else:
                st.error("Die gewählten Daten liegen außerhalb der verfügbaren Vorhersage.")
        else:
            st.error("Keine Daten zum Vergleichen verfügbar.")