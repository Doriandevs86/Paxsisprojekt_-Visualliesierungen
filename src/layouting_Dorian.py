import streamlit as st


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
                        "Globale Wetterkarte (coming soon)",
                        "Kontakt",
                        "Impressum"]
                        )


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


if page == "Wetterdaten":
    st.divider()
    st.header("Wetterdaten")



if page == "Wettervergleich":
    st.divider()
    st.header("Wettervergleich")


if page == "Globale WEtterkarte (coming soon)":
    st.divider()
    st.header("Globale WEtterkarte (coming soon)")


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