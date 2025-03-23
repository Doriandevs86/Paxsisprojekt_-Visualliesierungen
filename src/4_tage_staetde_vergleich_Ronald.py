import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
import seaborn as sns
from matplotlib.pyplot import title
from statsmodels.tsa.vector_ar.var_model import forecast

API_key = "Dein Api-Key"

def get_4days_2city(city):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error('Fehler beim Abrufen der Wetterdaten.')
        return None

st.sidebar.title('Welchen Zeitraum möchten Sie vergleichen?')
st.sidebar.markdown("")
page = st.sidebar.radio(" ",
                        ['4 Tages-Vergleich',
                        '16 Tages-Vergleich',
                        '30 Tages Klima-Vergleich']
                        )
# 4 Tages-Vergleich
if page == '4 Tages-Vergleich':


    st.title('4 Tagesvergleich von 2 Städten')

    city1 = st.text_input('Gib eine Stadt ein:', 'Berlin')
    city2 = st.text_input('Gib hier deine zweite Stadt ein:', 'Stuttgart')

    if st.button('Wetterdaten abrufen'):
        data = get_4days_2city(city1)
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
        data = get_4days_2city(city2)
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

#        lum_img = img[:, :, 0]
#        plt.imshow(lum_img)

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

        #        lum_img = img[:, :, 0]
        #        plt.imshow(lum_img)

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

        #        lum_img = img[:, :, 0]
        #        plt.imshow(lum_img)

            st.pyplot(fig)

