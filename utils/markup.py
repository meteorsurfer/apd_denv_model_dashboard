import streamlit as st 
from textwrap import dedent
from datetime import datetime, timezone
import plotly.express as px
import streamlit as st
import pydeck as pdk
import pandas as pd
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from .wrangling import enso_status_decoder
import requests

UTC_NOW = datetime.now(tz=timezone.utc)

from textwrap import dedent
import streamlit as st

def display_headline(
    text: str, 
    font_size: str = None, 
    text_align: str = "center", 
    font_color: str = "white"
):
    
    if not font_size:
        font_size = "2rem"

    body = dedent(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Be+Vietnam+Pro:wght@100..900&display=swap');
    .custom-header {{
        text-align: {text_align};
        font-size: {font_size};
        color: {font_color};
        font-family: "Be Vietnam Pro", sans-serif;
        padding-top: 0;
        margin-top: 0;
    }}
    </style>
    <div class="custom-header">{text}</div>
    <br>
    """)
    
    st.markdown(body, unsafe_allow_html=True)


def display_metadata(df_info):

    with st.expander("View Dataset Metadata", expanded=False):

        st.markdown("""
        ### 🌊 NOAA — Oceanic Niño Index (ONI)

        The [Oceanic Niño Index (ONI)](https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php) monitors **sea surface temperature anomalies** in the central tropical Pacific. It’s the gold standard for identifying **El Niño** and **La Niña** phases, which influence rainfall, temperature, and disease patterns globally.

        - **Use case**: Temporal feature for climate-driven outbreak modeling  
        - **Update frequency**: Monthly  
        - **Format**: Time series, anomaly values (°C)
        """)

        st.markdown("""
        ### ☀️ NASA — Historical Weather Features

        Climate variables are sourced from NASA’s [POWER Project](https://power.larc.nasa.gov/), offering **ML-ready solar, temperature, humidity, and rainfall data** for global locations.

        - **Use case**: Lagged weather features for dengue prediction  
        - **Access**: API or CSV download  
        - **Coverage**: Daily data, customizable by location
        """)

        st.markdown("""
        ### 🦟 DOH — Dengue Case Surveillance (Philippines)

        Dengue case counts are retrieved via the [FOI portal](https://www.foi.gov.ph/agencies/doh/dengue-cases-in-the-philippines-2016-to-2023/), covering **reported cases** across Philippine regions from **2016 to 2023**.

        - **Use case**: Ground truth for supervised learning  
        - **Format**: Tabular, region-wise 
        - **Note**: Data may require cleaning and harmonization
        """)

        st.markdown("""
        ### 🧪 WHO — Outbreak Classification Labels

        Outbreak levels are derived using the [WHO epidemic channel method](https://iris.who.int/bitstream/handle/10665/250240/9789241549738-eng.pdf), which flags abnormal spikes in dengue cases based on historical baselines.

        - **Use case**: Multi-class target labels (e.g., normal, elevated, outbreak)  
        - **Method**: Statistical thresholding over rolling averages  
        - **Interpretability**: Transparent and epidemiologically grounded
        """)

        st.dataframe(df_info, hide_index=True, height=560)
    return


def display_footer(utc_now=UTC_NOW):

    datum = UTC_NOW.strftime("%Y")


    body = dedent("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Be+Vietnam+Pro:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Josefin+Sans:ital,wght@0,100..700;1,100..700&family=Merriweather:ital,wght@0,300;0,400;0,700;0,900;1,300;1,400;1,700;1,900&family=Montserrat:ital,wght@0,100..900;1,100..900&family=Open+Sans:ital,wght@0,300..800;1,300..800&family=Orbitron:wght@400..900&family=Playwrite+IS:wght@100..400&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Quicksand:wght@300..700&display=swap');
    .custom-footer {
        text-align: center;
        font-size: 0.6rem;
        color: white;
        font-family: "Be Vietnam Pro", sans-serif;
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.1); 
        padding: 5px 0;
    }
    </style>
    <div class="custom-footer">
        © """+ datum +""" Developed by Alan Perry Daen — ML from Data Mining to Deployment
    </div>

    """
    )
    st.markdown(body, unsafe_allow_html=True)
    return


def visualize_denv_per_categories(df):

    categories = ["Region", "Month", "Year", "ENSO"]

    tab1, tab2, tab3, tab4 = st.tabs(categories)

    with tab1:
        df_loc = df.groupby("Region")["Cases"].median().reset_index().copy()
        fig = px.bar(
            df_loc,
            x="Region",
            y="Cases",
            color="Cases",
            color_continuous_scale="bluered",
            orientation="v",
            barmode="relative",
            height=560,
            title="<b>Median Dengue Cases Per Region</b><br><sup>Source: Department of Health 2016-2023</sup>",
        )
        fig.update_layout(title={"x": 0.5, "xanchor": "center", "yanchor": "top"})
        fig.update_xaxes(type="category")
        st.plotly_chart(fig, theme="streamlit", use_container_width=True, key="region")

    with tab2:
        df_month = df.groupby("Month")["Cases"].median().reset_index().copy()
        fig = px.bar(
            df_month,
            x="Month",
            y="Cases",
            color="Cases",
            color_continuous_scale="reds",
            orientation="v",
            barmode="relative",
            height=560,
            title="<b>Median Dengue Cases Per Month</b><br><sup>Source: Department of Health 2016-2023</sup>",
        )
        fig.update_layout(title={"x": 0.5, "xanchor": "center", "yanchor": "top"})
        st.plotly_chart(fig, theme="streamlit", use_container_width=True, key="month")

    with tab3:
        df_year = df.groupby("Year")["Cases"].median().reset_index().copy()
        fig = px.bar(
            df_year,
            x="Year",
            y="Cases",
            color="Cases",
            color_continuous_scale="blues",
            orientation="v",
            barmode="relative",
            height=560,
            title="<b>Median Dengue Cases Per Year</b><br><sup>Source: Department of Health 2016-2023</sup>",
        )
        fig.update_layout(title={"x": 0.5, "xanchor": "center", "yanchor": "top"})
        st.plotly_chart(fig, theme="streamlit", use_container_width=True, key="year")

    with tab4:
        df_enso = df.groupby("ENSO")["Cases"].median().reset_index().copy()
        df_enso["ENSO"] = df_enso["ENSO"].apply(enso_status_decoder)
        fig = px.bar(
            df_enso,
            x="ENSO",
            y="Cases",
            color="Cases",
            color_continuous_scale="purples",
            orientation="v",
            barmode="relative",
            height=560,
            title="<b>Median Dengue Cases Per ENSO</b><br><sup>Source: Department of Health 2016-2023</sup>",
        )
        fig.update_layout(title={"x": 0.5, "xanchor": "center", "yanchor": "top"})
        fig.update_xaxes(type="category")
        st.plotly_chart(fig, theme="streamlit", use_container_width=True, key="enso")

    return

def visualize_geographic_cases(df):
    
    capitals = df.groupby(["Region","lat","lon", "location"])["Cases"].median().reset_index()

    categories = ["Columnal", "Heatmap"]

    tab1, tab2 = st.tabs(categories)

    with tab1:

        norm = mcolors.Normalize(vmin=capitals["Cases"].min(), vmax=capitals["Cases"].max())
        cmap = cm.get_cmap("coolwarm")

        capitals["color"] = capitals["Cases"].apply(lambda x: [int(255*v) for v in cmap(norm(x))[:3]])
    
        capitals["size"] = capitals["Cases"] * 20
        capitals["elevation"] = capitals["Cases"] * 100

        point_layer = pdk.Layer(
            "ColumnLayer",
            data=capitals,
            get_position=["lon", "lat"],
            get_color="color",
            get_elevation="elevation",
            radius=20000,
            elevation_scale=1,
            pickable=True,
            auto_highlight=True,
        )

        view_state = pdk.ViewState(
            latitude=capitals["lat"].mean(),
            longitude=capitals["lon"].mean(),
            zoom=5.5,
            pitch=40,
            bearing=0
        )

        tooltip = {
            "html": """
            <b>Location:</b> {location}<br/>
            <b>Region:</b> {Region}<br/>
            <b>Lat:</b> {lat}<br/>
            <b>Lon:</b> {lon}<br/>
            <b>Median Cases:</b> {Cases}
            """,
            "style": {"backgroundColor": "steelblue", "color": "white"}
        }

        st.pydeck_chart(pdk.Deck(
            layers=[point_layer],
            initial_view_state=view_state,
            tooltip=tooltip
        ))

    with tab2:

        capitals = df.groupby(["Region", "lat", "lon"])["Cases"].median().reset_index()

        heatmap_layer = pdk.Layer(
            "HeatmapLayer",
            data=capitals,
            get_position=["lon", "lat"],
            get_weight="Cases",         
            radiusPixels=50,           
            intensity=0.8,                 
            threshold=0.04,             
            pickable=True
        )

        view_state = pdk.ViewState(
            latitude=capitals["lat"].mean(),
            longitude=capitals["lon"].mean(),
            zoom=4.5,
            pitch=40
        )


        st.pydeck_chart(pdk.Deck(
            layers=[heatmap_layer],
            initial_view_state=view_state,
            
        ))

def visualize_trend(df):
    df_trend = df.groupby(["Region", "Year"])["Cases"].median().reset_index().copy()
    fig = px.line(df_trend, x="Year", y="Cases", color='Region', markers=False)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True, key="trend")


def region_month_cases_density(df):
    df_trend = df.groupby(["Month", "Region"])["Cases"].median().reset_index().copy()
    fig = px.density_heatmap(
        df_trend,
        x='Month',
        y='Region',
        z='Cases',
        color_continuous_scale='YlOrRd',
        labels={'Cases': 'Median Cases'}
    )

    fig.update_layout(
        xaxis=dict(dtick=1),
        yaxis=dict(categoryorder='array', categoryarray=sorted(df['Region'].unique())),
        coloraxis_colorbar=dict(title='Cases')
    )
    fig.update_yaxes(type="category")
    fig.update_xaxes(type="category")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True, key="density")

def display_sample_outbreak_news(path):

    with st.expander("2019 Dengue Outbreak: Calabarzon Case Study", expanded=True):
        news = path + "philstar.png"
        news_1 = path + "outbreaks.png"
        st.image(image=news, caption="Dengue outbreak declared in Cavite (Source: Philippine Daily Inquirer)")
        st.image(image=news_1, caption="Dasmariñas posted the highest number of cases among cities in the region.")
    
    with st.expander("Show Historical Weather Data For Dengue Hotspots in April 2019", expanded=True):

        st.markdown("_Since the model is designed to forecast outbreak risk three months ahead, the weather data shown reflects conditions three months prior the outbreak declaration._")

        st.dataframe({
            "📍Location": ["Dasmarinas City, Cavite", "Calamba City, Laguna", "Lipa City, Batangas"],
            "📅Month": ["April", "April", "April"],
            "🌧️Rain (Total)": [35.64, 39.06, 39.06],
            "💧Humidity (Mean)": [64.94, 68.75, 68.75],
            "🌡️Temp. (Mean)": [30.08, 28.68, 28.68],
            "🌾ENSO Phase": ["Weak El Niño", "Weak El Niño", "Weak El Niño"]
        },hide_index=True)

        references = dedent("""
        <small><em>
        <strong>Data Source:</strong><br>
        The data was obtained from <a href="https://power.larc.nasa.gov/data-access-viewer/" target="_blank">NASA Langley Research Center's Prediction Of Worldwide Energy Resources (POWER)</a> project, funded through the NASA Earth Science Division.<br>
        Version: Monthly/Annual 2.x.x<br>
        Date Accessed: August 2025
        </em></small>
        """)

        st.markdown(references, unsafe_allow_html=True)

        #https://www.abs-cbn.com/news/health-science/2025/2/15/quezon-city-dengue-outbreak-10-deaths-over-1-700-cases-in-2-months-1703
        #recent outbreak

    return

def predict_dengue_risk_3_months():
    
    MODEL_API_URL = "https://my-dengue-ml.onrender.com/predict"

    months = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }


    regions = {
        'Cordillera Administrative Region': 'CAR',
        'Caraga Region': 'CARAGA',
        'Region 6': '6',
        'Region 5': '5',
        'Region 3': '3',
        'Bangsamoro Autonomous Region in Muslim Mindanao': 'BARMM',
        'Region 2': '2',
        'Region 4A': '4A',
        'Region 8': '8',
        'Region 7': '7',
        'Region 10': '10',
        'National Capital Region': 'NCR',
        'Region 9': '9',
        'Region 12': '12',
        'Region 1': '1',
        'Region 11': '11',
        'Region 4B': '4B'
    }

    ensos = {
        "Neutral": 0,
        "Weak La Niña": 1,
        "Moderate La Niña": 2,
        "Strong La Niña": 3,
        "Very Strong La Niña": 4,
        "Weak El Niño": 5,
        "Moderate El Niño": 6,
        "Strong El Niño": 7,
        "Very Strong El Niño": 8
    }

    payload = {
        "currentMonth": months[st.selectbox("Current Month", list(months.keys()))],
        "region": regions[st.selectbox("Region", list(regions.keys()))],
        "currentEnsoStatus": ensos[st.selectbox("Current ENSO Status", list(ensos.keys()))],
        "currentMonthlyTemperature": st.number_input("Current Mean Monthly Temperature"),
        "currentMonthlyRelativeHumidity": st.number_input("Current Mean Monthly Relative Humidity"),
        "currentMonthlyRainfall": st.number_input("Current Accumulated Monthly Rainfall")
    }

    if st.button("Predict"):
        response = requests.post(MODEL_API_URL, json=payload)
 
        if response.status_code == 200:
            try:
                result = response.json()
                st.write(result)
            except requests.exceptions.JSONDecodeError:
                st.error("Response was not valid JSON.")
                # st.write(response.text)
        else:
            st.error(f"API request failed with status code {response.status_code}")
            # st.write(response.text)


    return