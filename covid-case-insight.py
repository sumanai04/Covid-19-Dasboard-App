import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Set page config
st.set_page_config(layout='wide')

# Set plot style
sns.set_style("darkgrid")

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv")
    return df

# Streamlit App
st.title('COVID-19 Dashboard')
st.write('by Bagus Alwan Bambang - 22/492140/PA/21072 and Fathi Al Adha Hylmi - 22/492195/PA/21088')

# Load Data
data = load_data()

# Sidebar Input - Location Filter
selected_location = st.sidebar.selectbox('Select Location', data['location'].unique())

# Filter Data by Selected Location
filtered_data = data[data['location'] == selected_location]

fig = px.choropleth(data, locations="iso_code",
                    color="total_cases", 
                    hover_name="location", 
                    animation_frame="date",
                    title='Total COVID-19 Cases Over Time',
                    height=600,
                    width=1750)
st.plotly_chart(fig)
# Create two columns
col1, col2 = st.columns(2)

# Global Spread in column 1
with col1:
    # Pie Chart for Mortality Rate
    filtered_data['mortality_rate'] = (filtered_data['total_deaths'] / filtered_data['total_cases']) * 100
    mortality_rate_values = filtered_data['mortality_rate'].tail(1)  # Taking the latest mortality rate
    mortality_rate_values = mortality_rate_values.squeeze()  # Convert to scalar if possible
    if not pd.isnull(mortality_rate_values):
        fig_pie = px.pie(values=[mortality_rate_values, 100 - mortality_rate_values],
                        names=['Mortality Rate', 'Survival Rate'],
                        title=f'Mortality Rate for {selected_location}',
                        hole=0.5)
        st.plotly_chart(fig_pie)
    else:
        st.write('Mortality rate data is not available for the selected location.')

# Geographical Distributions - Total Deaths by Country in column 2
with col2:
    fig_geo = px.choropleth(filtered_data, 
                            locations='iso_code', 
                            color='total_deaths', 
                            hover_name='location',
                            projection='natural earth',
                            title='Geographical death distribution')
    st.plotly_chart(fig_geo)

st.header('Policy Response Effectiveness - Stringency Index Over Time')
fig_policy = px.line(filtered_data, x='date', y='stringency_index',
                        title='Stringency Index Over Time',
                        width=1750)
st.plotly_chart(fig_policy)

# Create two new columns
col5, col6 = st.columns(2)

# Trends in Cases and Deaths in column 5
with col5:
    cases_deaths_data = filtered_data[['date', 'total_cases', 'total_deaths']].copy()
    cases_deaths_data_melted = cases_deaths_data.melt(id_vars='date', value_vars=['total_cases', 'total_deaths'])
    fig_cases_deaths = px.line(cases_deaths_data_melted, x='date', y='value', color='variable',
                               labels={'value':'Number of People', 'variable':'Case Status'},
                               title='Trends in Cases and Deaths Over Time')
    st.plotly_chart(fig_cases_deaths)
with col6:
    vax_data = filtered_data[['date', 'people_vaccinated', 'people_fully_vaccinated', 'total_boosters']].copy()
    vax_data['partially_vaccinated'] = vax_data['people_vaccinated'] - vax_data['people_fully_vaccinated']
    vax_data_melted = vax_data.melt(id_vars='date', value_vars=['partially_vaccinated', 'people_fully_vaccinated', 'total_boosters'])
    fig_vax = px.area(vax_data_melted, x='date', y='value', color='variable',
                      labels={'value':'Number of People', 'variable':'Vaccination Status'},
                      title='Vaccination Progress Over Time')
    st.plotly_chart(fig_vax)