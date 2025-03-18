import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


# Api_key
api_key = "3986444df517b61fd9c0b7ec2ea4561c"


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


# Funktion für 16 Tage-Vorhersagen
def fetch_16d_forecast(city):
    forecast_16d_url = "http://api.openweathermap.org/data/2.5/forecast/daily"
    params = {
        "q": city,
        "cnt": 16,  # Anzahl der Tage
        "appid": api_key,
        "units": "metric",
        "lang": "de"
    }
    response = requests.get(forecast_16d_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Fehler beim Abrufen der 16-Tages-Vorhersage")
        return None


# # Funktion, um historische Wetterdaten abzurufen
# def get_historical_weather(city, date):
#     # Umwandlung des Datums in Unix-Timestamp
#     timestamp = int(datetime.strptime(date, "%Y-%m-%d").timestamp())
#
#     # URL für die API-Anfrage
#     url = f"http://api.openweathermap.org/data/2.5/onecall/timemachine"
#
#     # Parameter für die Anfrage
#     params = {
#         'lat': city['lat'],
#         'lon': city['lon'],
#         'dt': timestamp,
#         'appid': api_key
#     }
#
#     response = requests.get(url, params=params)
#     data = response.json()
#
#     if response.status_code == 200:
#         # Extrahiere relevante Wetterdaten
#         weather_data = data.get('hourly', [])
#         df = pd.DataFrame(weather_data)
#         return df
#     else:
#         st.error(f"Fehler bei der API-Anfrage: {data.get('message')}")
#         return None


def get_emoji_for_weather(value, category):
    # Temperatur Emojis
    if category == "temperature":
        if value < 0:
            return "❄️"
        elif 0 <= value <= 10:
            return "🌧️"
        elif 10 < value <= 20:
            return "☀️"
        elif 20 < value <= 30:
            return "🌞"
        else:
            return "🔥"

    # Luftfeuchtigkeit Emojis
    elif category == "humidity":
        if value < 20:
            return "💨"
        elif 20 <= value < 40:
            return "🌵"
        elif 40 <= value < 60:
            return "🌤️"
        elif 60 <= value < 80:
            return "🌧️"
        else:
            return "🌧️💦"

    # Windgeschwindigkeit Emojis
    elif category == "wind_speed":
        if value < 10:
            return "🍃"
        elif 10 <= value < 30:
            return "🌬️"
        elif 30 <= value < 50:
            return "🌪️"
        else:
            return "🌫️"

    # UV-Index Emojis
    elif category == "uv_index":
        if value < 3:
            return "😎"
        elif 3 <= value < 6:
            return "🌞"
        elif 6 <= value < 8:
            return "🌅"
        elif 8 <= value < 11:
            return "☠️"
        else:
            return "🔥"

    else:
        return "🌍"


st.title("Praxisprojekt Datenvisualisierung")

st.sidebar.title("Navigation")
st.sidebar.markdown("")
page = st.sidebar.radio(" ",
                        ["Startseite",
                        "Wetterdaten",
                        "Wettervergleich",
                        "Städtevergleich",
                        "Globale Wetterkarte (coming soon)",
                        "Kontakt",
                        "Impressum"]
                        )

# Inhalte der Sidebar

if page == "Startseite":
    st.divider()
    st.header("Startseite")
    st.write(""" 
        Herzlich willkommen auf der Plattform für umfassende Wetterdaten und -analysen. Diese Seite bietet Ihnen eine 
        benutzerfreundliche Möglichkeit, auf verschiedene Wetterinformationen zuzugreifen und detaillierte Auswertungen
        zu betrachten. Unsere Navigation auf der linken Seite ermöglicht Ihnen den einfachen Zugang zu den verschiedenen
        Rubriken:

        - **Wetterdaten**: Hier können Sie aktuelle Wetterdaten wie Temperatur, Luftfeuchtigkeit und Windgeschwindigkeit
        einsehen. Zudem bieten wir eine "Wetter-App", mit der Sie Wetterprognosen für verschiedene Zeiträume anzeigen 
        lassen können.

        - **Auswertungen**: In diesem Bereich haben Sie die Möglichkeit, verschiedene Wetterdaten miteinander zu vergleichen.
        Beispielsweise können Sie Städte oder Regionen anhand von historischen und aktuellen Daten miteinander vergleichen,
        um interessante Trends und Veränderungen zu erkennen.

        - **Globale Wetterkarte**: Auf der interaktiven globalen Wetterkarte können Sie die aktuelle Temperatur weltweit
        auf einem anschaulichen Globus visualisieren. Diese Karte bietet eine beeindruckende Möglichkeit, das 
        Wettergeschehen auf einen Blick zu verfolgen.

        - **Kontakt**: Falls Sie Fragen oder Anregungen haben, können Sie uns jederzeit über unsere Kontaktseite erreichen.

        - **Impressum**: Alle rechtlichen Informationen finden Sie unter unserem Impressum.

        Wir wünschen Ihnen viel Spaß beim Erkunden der Plattform und hoffen, dass Sie die gewünschten Informationen 
        schnell und bequem finden!
    """)
st.divider()

### Seite Wetterdaten ###
if page == "Wetterdaten":

    st.header("Wetterdaten")

    col2, col1 = st.columns(2)

    with col1:
        st.markdown("<h4>Gib eine Stad ein:</h4>", unsafe_allow_html=True)
        city = st.text_input("", "Berlin")

    with col2:
        st.markdown("<h4>Triff deine Auswahl</h4>", unsafe_allow_html=True)
        weather_type = st.radio("",
                                ("Aktuelles Wetter",
                                "3 Stundenintervall Heute",
                                "Wettervorhersage für die nächsten 5 Tage",
                                "Wettervorhersage für die nächsten 16 Tage",
                                "Benutzerdefinierter Zeitraum")
                                )
    st.divider()

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

            # Emoji zuordnen
            temperature_emoji = get_emoji_for_weather(temperature, "temperature")
            humidity_emoji = get_emoji_for_weather(humidity, "humidity")
            wind_emoji = get_emoji_for_weather(wind_speed, "wind_speed")

            st.markdown("<h5>Aktuelles Wetter in:</h5>", unsafe_allow_html=True)
            st.write(f"**Stadt:** {city_name}")
            st.write(f"**Wetterlage:** {description}")
            st.write(f"**Temperatur:** {temperature} °C {temperature_emoji}")
            st.write(f"**Luftfeuchtigkeit:** {humidity} % {humidity_emoji}")
            st.write(f"**Windgeschwindigkeit:** {wind_speed} m/s {wind_emoji}")
            st.divider()

            # DataFrame
            current_weather_df = pd.DataFrame({
                "Rubrik": ["Temperatur", "Luftfeuchtigkeit", "Beschreibung", "Windgeschwindigkeit"],
                "Wert": [f"{temperature} °C", f"{humidity} %", description, f"{wind_speed} m/s"]
            })

            st.dataframe(current_weather_df)


    # Wettervorhersage für die nächsten 3 Stunden anzeigen
    elif weather_type == "3 Stundenintervall Heute" and city:
        forecast_3h_data = fetch_5d_forecast(city)
        if forecast_3h_data:
            st.write(f"### 3 Stundenintervall heute in {city}:")

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

            st.markdown("<h4>Wählen Sie eine Rubrik:</h4>", unsafe_allow_html=True)

            chart_type = st.selectbox(
                "",
                ["Temperatur in Celsius", "Luftfeuchtigkeit in %", "Windgeschwindigkeit in m/s"]
            )


            # Temperatur-Diagramm
            if chart_type == "Temperatur in Celsius":
                fig, ax = plt.subplots()
                ax.plot(time_list, temp_list, marker='o', color='tab:red')
                ax.set_title("Temperatur im 3-Stunden-Intervall")
                ax.set_xlabel("Uhrzeit")
                ax.set_ylabel("Temperatur (°C)")
                plt.xticks(rotation=45)
                st.pyplot(fig)

            # Luftfeuchtigkeit-Diagramm
            elif chart_type == "Luftfeuchtigkeit in %":
                fig, ax = plt.subplots()
                ax.bar(time_list, humidity_list, color='tab:cyan')
                ax.set_title("Luftfeuchtigkeit im 3-Stunden-Intervall")
                ax.set_xlabel("Uhrzeit")
                ax.set_ylabel("Luftfeuchtigkeit (%)")
                plt.xticks(rotation=45)
                st.pyplot(fig)

            # Windgeschwindigkeit-Diagramm
            elif chart_type == "Windgeschwindigkeit in m/s":
                fig, ax = plt.subplots()
                ax.fill_between(time_list, wind_list, color='tab:green', alpha=0.5)
                ax.set_title("Windgeschwindigkeit im 3-Stunden-Intervall")
                ax.set_xlabel("Uhrzeit")
                ax.set_ylabel("Windgeschwindigkeit (m/s)")
                plt.xticks(rotation=45)
                st.pyplot(fig)
                # st.dataframe(forecast_3h_df)



    # Wettervorhersage für die nächsten 5 Tage
    elif weather_type == "Wettervorhersage für die nächsten 5 Tage" and city:
        forecast_5d_data = fetch_5d_forecast(city)
        if forecast_5d_data and city:

            st.write(f"### Wettervorhersage für die nächsten 5 Tage in {city}:")

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

            st.markdown("<h4>Wählen Sie eine Rubrik:</h4>", unsafe_allow_html=True)

            chart_type1 = st.selectbox(
                "",
                ["Temperatur in Celsius", "Luftfeuchtigkeit in %", "Windgeschwindigkeit in m/s"]
            )

            # Diagramme
            if chart_type1 == "Temperatur in Celsius":
                fig, ax = plt.subplots()
                ax.plot(grouped_df['Datum'], grouped_df['Temperatur'], marker='o', color='tab:red')
                ax.set_xlabel("Datum")
                ax.set_ylabel("Temperatur (°C)")
                plt.xticks(rotation=45)
                st.pyplot(fig)

            elif chart_type1 == "Luftfeuchtigkeit in %":
                fig, ax = plt.subplots()
                ax.bar(grouped_df['Datum'], grouped_df['Luftfeuchtigkeit'], color='tab:cyan')
                ax.set_xlabel("Datum")
                ax.set_ylabel("Luftfeuchtigkeit (%)")
                plt.xticks(rotation=45)
                st.pyplot(fig)

            elif chart_type1 == "Windgeschwindigkeit in m/s":
                fig, ax = plt.subplots()
                ax.fill_between(grouped_df['Datum'], grouped_df['Windgeschwindigkeit'], alpha=0.4, color='tab:green')
                ax.set_xlabel("Datum")
                ax.set_ylabel("Windgeschwindigkeit (m/s)")
                plt.xticks(rotation=45)
                st.pyplot(fig)

            # st.dataframe(grouped_df)


    # Wettervorhersage für die nächsten 16 Tage
    elif weather_type == "Wettervorhersage für die nächsten 16 Tage" and city:
        forecast_16d_data = fetch_16d_forecast(city)
        if forecast_16d_data:
            st.write(f"### Wettervorhersage für die nächsten 16 Tage in {city}:")

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

            st.markdown("<h4>Wählen Sie eine Rubrik:</h4>", unsafe_allow_html=True)

            chart_type2 = st.selectbox(
                "",
                ["Temperatur in Celsius", "Luftfeuchtigkeit in %", "Windgeschwindigkeit in m/s"]
            )
            # Temperatur-Diagramm
            if chart_type2 == "Temperatur in Celsius":
                fig, ax = plt.subplots()
                ax.plot(date_list, temp_list, marker='o', color='tab:red')
                ax.set_title("Temperatur über die nächsten Tage")
                ax.set_xlabel("Datum")
                ax.set_ylabel("Temperatur (°C)")
                ax.set_xticks(date_list[::2])
                plt.xticks(rotation=45)
                st.pyplot(fig)

            # Luftfeuchtigkeit-Diagramm
            elif chart_type2 == "Luftfeuchtigkeit in %":
                fig, ax = plt.subplots()
                ax.bar(date_list, humidity_list, color='tab:cyan')
                ax.set_title("Luftfeuchtigkeit über die nächsten Tage")
                ax.set_xlabel("Datum")
                ax.set_ylabel("Luftfeuchtigkeit (%)")
                ax.set_xticks(date_list[::2])
                plt.xticks(rotation=45)
                st.pyplot(fig)

            # Windgeschwindigkeit-Diagramm
            elif chart_type2 == "Windgeschwindigkeit in m/s":
                fig, ax = plt.subplots()
                ax.fill_between(date_list, wind_list, color='tab:green', alpha=0.5)
                ax.set_title("Windgeschwindigkeit über die nächsten Tage")
                ax.set_xlabel("Datum")
                ax.set_ylabel("Windgeschwindigkeit (m/s)")
                ax.set_xticks(date_list[::2])
                plt.xticks(rotation=45)
                st.pyplot(fig)

                    # st.dataframe(forecast_16d_df)


    # Benutzerdefinierter Zeitraum
    elif weather_type == "Benutzerdefinierter Zeitraum" and city:
        st.write("### Wettervorhersage für deinen Zeitraum")

        start_date = st.date_input("Startdatum", value=pd.to_datetime("today").date())
        end_date = st.date_input("Enddatum", value=pd.to_datetime("today").date())

        # Button zum Abrufen der Daten
        if st.button("Daten abrufen"):
            if start_date > end_date:
                st.error("Das Startdatum darf nicht nach dem Enddatum liegen.")
            else:
                forecast_16d_data = fetch_16d_forecast(city)
                if forecast_16d_data:
                    # Listen zum Speichern der Wetterdaten
                    date_list, temp_list, humidity_list, wind_list, description_list = [], [], [], [], []

                    for day in forecast_16d_data['list']:
                        date = pd.to_datetime(day['dt'], unit='s').date()
                        if start_date <= date <= end_date:
                            temp = day['temp']['day']
                            humidity = day['humidity']
                            description = day['weather'][0]['description']
                            wind_speed = day['speed']

                            date_list.append(date)
                            temp_list.append(temp)
                            humidity_list.append(humidity)
                            wind_list.append(wind_speed)
                            description_list.append(description)

                    # Speichern der Wetterdaten im Session State
                    st.session_state["forecast_16d_df"] = pd.DataFrame({
                        "Datum": date_list,
                        "Temperatur": [f"{t}°C" for t in temp_list],
                        "Luftfeuchtigkeit": [f"{h}%" for h in humidity_list],
                        "Beschreibung": description_list,
                        "Windgeschwindigkeit": [f"{w} m/s" for w in wind_list]
                    })

                    st.session_state["date_list"] = date_list
                    st.session_state["temp_list"] = temp_list
                    st.session_state["humidity_list"] = humidity_list
                    st.session_state["wind_list"] = wind_list

                else:
                    st.error("Es konnten keine Daten abgerufen werden.")

        # Prüfe, ob Wetterdaten im Session State existieren
        if "forecast_16d_df" in st.session_state:
            st.write("### Wetterdaten")
            st.dataframe(st.session_state["forecast_16d_df"])

            # Diagrammoptionen
            st.markdown("<h4>Wählen Sie eine Rubrik:</h4>", unsafe_allow_html=True)
            chart_type8 = st.selectbox("",
                                       ["Temperatur in Celsius", "Luftfeuchtigkeit in %", "Windgeschwindigkeit in m/s"])

            # Daten abrufen aus dem Session State
            date_list = st.session_state["date_list"]
            temp_list = st.session_state["temp_list"]
            humidity_list = st.session_state["humidity_list"]
            wind_list = st.session_state["wind_list"]

            # Temperatur-Diagramm
            if chart_type8 == "Temperatur in Celsius":
                fig, ax = plt.subplots()
                ax.plot(date_list, temp_list, marker='o', color='tab:red')
                ax.set_title("Temperatur über die nächsten Tage")
                ax.set_xlabel("Datum")
                ax.set_ylabel("Temperatur (°C)")
                plt.xticks(rotation=45)
                st.pyplot(fig)

            # Luftfeuchtigkeit-Diagramm
            elif chart_type8 == "Luftfeuchtigkeit in %":
                fig, ax = plt.subplots()
                ax.bar(date_list, humidity_list, color='tab:cyan')
                ax.set_title("Luftfeuchtigkeit über die nächsten Tage")
                ax.set_xlabel("Datum")
                ax.set_ylabel("Luftfeuchtigkeit (%)")
                plt.xticks(rotation=45)
                st.pyplot(fig)

            # Windgeschwindigkeit-Diagramm
            elif chart_type8 == "Windgeschwindigkeit in m/s":
                fig, ax = plt.subplots()
                ax.fill_between(date_list, wind_list, color='tab:green', alpha=0.5)
                ax.set_title("Windgeschwindigkeit über die nächsten Tage")
                ax.set_xlabel("Datum")
                ax.set_ylabel("Windgeschwindigkeit (m/s)")
                plt.xticks(rotation=45)
                st.pyplot(fig)

                # st.dataframe(forecast_16d_df)


    # Überprüfen, ob die Daten bereits im session_state gespeichert sind
    elif 'forecast_16d_df' in st.session_state:
        forecast_16d_df = st.session_state.forecast_16d_df
        date_list = st.session_state.date_list
        temp_list = st.session_state.temp_list
        humidity_list = st.session_state.humidity_list
        wind_list = st.session_state.wind_list

        st.markdown("<h4>Wählen Sie eine Rubrik:</h4>", unsafe_allow_html=True)

        chart_type3 = st.selectbox(
            "",
            ["Temperatur in Celsius", "Luftfeuchtigkeit in %", "Windgeschwindigkeit in m/s"]
        )
        # Temperatur-Diagramm
        if chart_type3 == "Temperatur in Celsius":
            fig, ax = plt.subplots()
            ax.plot(date_list, temp_list, marker='o', color='tab:red')
            ax.set_title("Temperatur über die nächsten Tage")
            ax.set_xlabel("Datum")
            ax.set_ylabel("Temperatur (°C)")
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # Luftfeuchtigkeit-Diagramm
        elif chart_type3 == "Luftfeuchtigkeit in %":
            fig, ax = plt.subplots()
            ax.bar(date_list, humidity_list, color='tab:cyan')
            ax.set_title("Luftfeuchtigkeit über die nächsten Tage")
            ax.set_xlabel("Datum")
            ax.set_ylabel("Luftfeuchtigkeit (%)")
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # Windgeschwindigkeit-Diagramm
        elif chart_type3 == "Windgeschwindigkeit in m/s":
            fig, ax = plt.subplots()
            ax.fill_between(date_list, wind_list, color='tab:green', alpha=0.5)
            ax.set_title("Windgeschwindigkeit über die nächsten Tage")
            ax.set_xlabel("Datum")
            ax.set_ylabel("Windgeschwindigkeit (m/s)")
            plt.xticks(rotation=45)
            st.pyplot(fig)
        st.divider()


# Wettervergleichsseite
if page == "Wettervergleich":
    city = st.text_input("Stadt eingeben", "Berlin")

    start_date = st.date_input("Startdatum", value=pd.to_datetime("today").date())
    end_date = st.date_input("Enddatum", value=pd.to_datetime("today").date())

    # Daten nur einmal abrufen und speichern
    if st.button("Daten vergleichen"):
        forecast_data = fetch_16d_forecast(city)
        if forecast_data:
            st.session_state['forecast_data'] = forecast_data
        else:
            st.error("Keine Daten zum Vergleichen verfügbar.")

    if 'forecast_data' in st.session_state:
        forecast_data = st.session_state['forecast_data']
        all_dates = [datetime.fromtimestamp(day['dt']).date() for day in forecast_data['list']]

        # Indizes für den gewählten Zeitraum finden
        start_idx = next((i for i, d in enumerate(all_dates) if d >= start_date), None)
        end_idx = next((i for i, d in enumerate(all_dates) if d >= end_date), None)

        st.divider()

        if start_idx is not None and end_idx is not None:
            dates = all_dates[start_idx:end_idx + 1]
            temp_list = [forecast_data['list'][i]['temp']['day'] for i in range(start_idx, end_idx + 1)]
            humidity_list = [forecast_data['list'][i]['humidity'] for i in range(start_idx, end_idx + 1)]
            wind_list = [forecast_data['list'][i]['speed'] for i in range(start_idx, end_idx + 1)]

            # Auswahl des Diagrammtyps
            st.write(f"### Wetterentwicklung in {city} \n ### von {start_date} bis {end_date}")

            st.markdown("<h4>Wählen Sie eine Rubrik:</h4>", unsafe_allow_html=True)

            chart_type4 = st.selectbox("",[
                                        "Temperatur in Celsius",
                                        "Luftfeuchtigkeit in %",
                                        "Windgeschwindigkeit in m/s"])


            # Matplotlib-Diagramme
            fig, ax = plt.subplots()
            if chart_type4 == "Temperatur in Celsius":
                ax.plot(dates, temp_list, marker='o', color='tab:red')
                ax.set_ylabel("Temperatur (°C)")
                ax.set_title(f"Temperatur in {city}")
            elif chart_type4 == "Luftfeuchtigkeit in %":
                ax.bar(dates, humidity_list, color='tab:cyan')
                ax.set_ylabel("Luftfeuchtigkeit (%)")
                ax.set_title(f"Luftfeuchtigkeit in {city}")
            elif chart_type4 == "Windgeschwindigkeit in m/s":
                ax.fill_between(dates, wind_list, color='tab:green', alpha=0.5)
                ax.set_ylabel("Windgeschwindigkeit (m/s)")
                ax.set_title(f"Windgeschwindigkeit in {city}")

            ax.set_xlabel("Datum")
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # Vergleich zwischen Start- und Enddatum
            start_data = forecast_data['list'][start_idx]
            end_data = forecast_data['list'][end_idx]

            vergleichs_df = pd.DataFrame({
                "Parameter": ["Temperatur (°C)", "Luftfeuchtigkeit (%)", "Windgeschwindigkeit (m/s)"],
                f"{start_date}": [start_data['temp']['day'], start_data['humidity'], start_data['speed']],
                f"{end_date}": [end_data['temp']['day'], end_data['humidity'], end_data['speed']]
            })

            st.divider()
            st.write(f"### Vergleichsdiagramm des Wetters in {city} \n zwischen {start_date} und {end_date}")
            st.dataframe(vergleichs_df)

            # Vergleichs-Diagramm
            plt.style.use("dark_background")
            fig, ax = plt.subplots()
            vergleichs_df.set_index("Parameter").plot(kind="bar", color=['#1f77b4', '#17becf'], ax=ax)
            ax.set_title(f"Wettervergleich in {city} zwischen {start_date} und {end_date}", color='white')
            ax.set_xlabel("Parameter", color='white')
            ax.set_ylabel("Wert", color='white')
            ax.tick_params(axis='x', colors='white', rotation=0)
            ax.tick_params(axis='y', colors='white')

            fig.tight_layout()

            st.pyplot(fig)
        else:
            st.error("Die gewählten Daten liegen außerhalb der verfügbaren Vorhersage.")



# Städtevergleichsseite
if page == "Städtevergleich":
    st.sidebar.title('Welchen Zeitraum möchten Sie vergleichen?')
    page = st.sidebar.radio(" ",
                            ['4 Tages-Vergleich',
                             '16 Tages-Vergleich',
                             '30 Tages-Vergleich']
                            )
    # 4 Tages-Vergleich
    if page == '4 Tages-Vergleich':
        st.title('Welche beiden Städte möchtest du vergleichen?')
        city1 = st.text_input('Gib eine Stadt ein:', 'Berlin')
        city2 = st.text_input('Gib hier deine zweite Stadt ein:', 'Stuttgart')

        if st.button('Wetterdaten abrufen'):
            data = fetch_5d_forecast(city1)
            if data:
                forecast_list = data['list']
                city = data['city']['name']
                dates = [item['dt_txt'] for item in forecast_list]
                temps = [item['main']['temp'] for item in forecast_list]
                wind_speed = [item['wind']['speed'] for item in forecast_list]
                humidity = [item['main']['humidity'] for item in forecast_list]
                df1 = pd.DataFrame({
                    'Stadt': city,
                    'Datum': pd.to_datetime(dates),
                    'Temperatur (°C)': temps,
                    'Windgeschwindigkeit (m/s)': wind_speed,
                    'Luftfeuchtigkeit (%)': humidity
                })
            data = fetch_5d_forecast(city2)
            if data:
                forecast_list = data['list']
                city = data['city']['name']
                dates = [item['dt_txt'] for item in forecast_list]
                temps = [item['main']['temp'] for item in forecast_list]
                wind_speed = [item['wind']['speed'] for item in forecast_list]
                humidity = [item['main']['humidity'] for item in forecast_list]
                df2 = pd.DataFrame({
                    'Stadt': city1,
                    'Datum': pd.to_datetime(dates),
                    'Temperatur (°C)': temps,
                    'Windgeschwindigkeit (m/s)': wind_speed,
                    'Luftfeuchtigkeit (%)': humidity
                })

            plt.style.use("dark_background")

            st.write("Wähle eine Rubrik")
            # Tabs auf dem Plot
            tab1, tab2, tab3 = st.tabs(['Temperatur',
                                        'Windgeschwindigkeit',
                                        'Luftfeuchtigkeit'])

            with tab1:
                st.header('Temperatur')
                fig, ax = plt.subplots()
                ax.plot(df1['Datum'], df1['Temperatur (°C)'], color='b')
                ax.plot(df2['Datum'], df2['Temperatur (°C)'], color='c')
                plt.xticks(rotation=45)
                plt.xlabel('Datum')
                plt.ylabel('Temperatur (°C)')
                ax.legend(labels=[city1, city])
                st.pyplot(fig)

            with tab2:
                st.header('Windgeschwindigkeit')
                fig, ax = plt.subplots()
                ax.plot(df1['Datum'], df1['Windgeschwindigkeit (m/s)'], color='b')
                ax.plot(df2['Datum'], df2['Windgeschwindigkeit (m/s)'], color='c')
                plt.xticks(rotation=45)
                plt.xlabel('Datum')
                plt.ylabel('Windgeschwindigkeit (m/s)')
                ax.legend(labels=[city1, city])
                st.pyplot(fig)

            with tab3:
                st.header('Luftfeuchtigkeit')
                fig, ax = plt.subplots()
                ax.plot(df1['Datum'], df1['Luftfeuchtigkeit (%)'], color='b')
                ax.plot(df2['Datum'], df2['Luftfeuchtigkeit (%)'], color='c')
                plt.xticks(rotation=45)
                plt.xlabel('Datum')
                plt.ylabel('Luftfeuchtigkeit (%)')
                ax.legend(labels=[city1, city])
                st.pyplot(fig)

    if page == '16 Tages-Vergleich':
        st.title('Welche beiden Städte möchtest du vergleichen?')
        city1 = st.text_input('Gib eine Stadt ein:', 'Berlin')
        city2 = st.text_input('Gib hier deine zweite Stadt ein:', 'Stuttgart')

        if st.button('Wetterdaten abrufen'):
            data1 = fetch_16d_forecast(city1)
            data2 = fetch_16d_forecast(city2)

            # Stadt 1 Daten extrahieren
            if data1:
                forecast_list1 = data1['list']
                city1_name = data1['city']['name']

                # Listen zur Speicherung der Wetterdaten
                date_list1 = []
                temp_list1 = []
                humidity_list1 = []
                wind_list1 = []
                description_list1 = []

                for day in forecast_list1:
                    date = pd.to_datetime(day['dt'], unit='s').strftime('%Y-%m-%d')
                    temp = day['temp']['day']
                    humidity = day['humidity']
                    description = day['weather'][0]['description']
                    wind_speed = day['speed']

                    date_list1.append(date)
                    temp_list1.append(temp)
                    humidity_list1.append(humidity)
                    wind_list1.append(wind_speed)
                    description_list1.append(description)

                df1 = pd.DataFrame({
                    'Stadt': city1_name,
                    'Datum': date_list1,
                    'Temperatur (°C)': temp_list1,
                    'Luftfeuchtigkeit (%)': humidity_list1,
                    'Windgeschwindigkeit (m/s)': wind_list1,
                    'Beschreibung': description_list1
                })

            # Stadt 2 Daten extrahieren
            if data2:
                forecast_list2 = data2['list']
                city2_name = data2['city']['name']

                # Listen zur Speicherung der Wetterdaten
                date_list2 = []
                temp_list2 = []
                humidity_list2 = []
                wind_list2 = []
                description_list2 = []

                for day in forecast_list2:
                    date = pd.to_datetime(day['dt'], unit='s').strftime('%Y-%m-%d')
                    temp = day['temp']['day']
                    humidity = day['humidity']
                    description = day['weather'][0]['description']
                    wind_speed = day['speed']

                    date_list2.append(date)
                    temp_list2.append(temp)
                    humidity_list2.append(humidity)
                    wind_list2.append(wind_speed)
                    description_list2.append(description)

                df2 = pd.DataFrame({
                    'Stadt': city2_name,
                    'Datum': date_list2,
                    'Temperatur (°C)': temp_list2,
                    'Luftfeuchtigkeit (%)': humidity_list2,
                    'Windgeschwindigkeit (m/s)': wind_list2,
                    'Beschreibung': description_list2
                })

            st.write("Wähle eine Rubrik")
            # Visualisierung
            plt.style.use("dark_background")

            # Tabs auf dem Plot
            tab1, tab2, tab3 = st.tabs(['Temperatur', 'Windgeschwindigkeit', 'Luftfeuchtigkeit'])

            with tab1:
                st.header('Temperatur')
                fig, ax = plt.subplots()
                ax.plot(df1['Datum'], df1['Temperatur (°C)'], color='b', label=city1_name)
                ax.plot(df2['Datum'], df2['Temperatur (°C)'], color='c', label=city2_name)
                ax.set_xticks(df1['Datum'][::2])
                plt.xticks(rotation=45)
                plt.xlabel('Datum')
                plt.ylabel('Temperatur (°C)')
                ax.legend()
                st.pyplot(fig)

            with tab2:
                st.header('Windgeschwindigkeit')
                fig, ax = plt.subplots()
                ax.plot(df1['Datum'], df1['Windgeschwindigkeit (m/s)'], color='b', label=city1_name)
                ax.plot(df2['Datum'], df2['Windgeschwindigkeit (m/s)'], color='c', label=city2_name)
                ax.set_xticks(df1['Datum'][::2])
                plt.xticks(rotation=45)
                plt.xlabel('Datum')
                plt.ylabel('Windgeschwindigkeit (m/s)')
                ax.legend()
                st.pyplot(fig)

            with tab3:
                st.header('Luftfeuchtigkeit')

                fig, ax = plt.subplots()
                ax.plot(df1['Datum'], df1['Luftfeuchtigkeit (%)'], color='b', label=city1_name)
                ax.plot(df2['Datum'], df2['Luftfeuchtigkeit (%)'], color='c', label=city2_name)
                ax.set_xticks(df1['Datum'][::2])
                plt.xticks(rotation=45)
                plt.xlabel('Datum')
                plt.ylabel('Luftfeuchtigkeit (%)')
                ax.legend()
                st.pyplot(fig)


    if page == '30 Tages-Vergleich':
        st.title('---Work in progress---')
        st.write("## Coming soon")


# Wetterkarte
if page == "Globale Wetterkarte (coming soon)":
    st.title('Interaktive Wetterkarte')
    st.write("## -----------   WORK IN PROGRESS  ----------")

    ## Benutzereingabe für die Stadt
    # city = st.text_input("Gib eine Stadt ein:", "Berlin")
    #
    # if st.button("Wetter anzeigen"):
    #        # Karte erstellen
    #        m = folium.Map(location=[lat, lon], zoom_start=10)
    #        folium.Marker(
    #            [lat, lon],
    #            popup=popup_text,
    #            tooltip=city,
    #            icon=folium.Icon(color="blue", icon="info-sign")
    #        ).add_to(m)
    #
    #        # Karte in Streamlit anzeigen
    #        st_folium(m, width=700, height=500)
    #         -----------   WORK IN PROGRESS  -----------


### Kontakt Seite ###
if page == "Kontakt":
    st.header("Kontaktieren Sie uns")
    st.write("""
        Vielen Dank für Ihr Interesse an unserer Plattform. Wenn Sie Fragen, Anregungen oder Feedback haben, zögern Sie
        bitte nicht, uns zu kontaktieren. 

        Wir stehen Ihnen gerne zur Verfügung.

        **Max Mustermann**

        - **E-Mail:** max.mustermann@email.de
        - **Telefon:** 01234 56789
        - **Adresse:** Musterstraße 123, 12345 Musterstadt

        Wir bemühen uns, Ihre Anfrage so schnell wie möglich zu beantworten!
        """, unsafe_allow_html=True)
    st.divider()



### Impressum Seite ###
if page == "Impressum":
    st.header("Impressum")
    st.write("""
        Angaben gemäß § 5 TMG:<br>

        Max Mustermann<br>
        Musterstraße 123<br>
        12345 Musterstadt<br>
        Telefon: 01234 56789<br>
        E-Mail: max.mustermann@email.de<br><br>
        """, unsafe_allow_html=True)
    st.divider()
    st.write("""
        Umsatzsteuer-Identifikationsnummer gemäß § 27 a Umsatzsteuergesetz: DE123456789

        Verantwortlich für den Inhalt nach 17 Abs. 2 i.V.m. § 18 Abs. 2 MStV:
        Max Mustermann (Adresse wie oben)

        Haftungsausschluss:
        Die Inhalte dieser Website wurden mit größter Sorgfalt erstellt. Für die Richtigkeit, Vollständigkeit und Aktualität
        der Inhalte können jedoch keine Gewähr übernommen werden.

        Externe Links:
        Diese Website enthält Links zu externen Webseiten Dritter. Auf den Inhalt dieser Seiten haben wir keinen Einfluss.
        Deshalb können wir für diese fremden Inhalte keine Gewähr übernehmen.
        """)
    st.divider()