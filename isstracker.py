import streamlit as st
import requests
import pandas as pd
import plotly.express as px

def fetch_iss_location():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    if response.status_code == 200:
        data = response.json()
        return data['iss_position']
    else:
        return None

def fetch_astros():
    response = requests.get("http://api.open-notify.org/astros.json")
    if response.status_code == 200:
        return response.json()
    else:
        return None

def main():
    st.title('Live ISS Tracker and Astronaut Info')

    # Display ISS location first
    st.subheader("Current Location of the ISS")
    position = fetch_iss_location()
    if position:
        latitude = float(position['latitude'])
        longitude = float(position['longitude'])
        st.write(f"Latitude: {latitude}, Longitude: {longitude}")
        df = pd.DataFrame([{'lat': latitude, 'lon': longitude}])
        fig = px.scatter_geo(df, lat='lat', lon='lon', 
                             projection="natural earth",
                             title="ISS Location on Earth")
        st.plotly_chart(fig)
    else:
        st.error("Failed to retrieve ISS location.")

    # Display astronauts information below ISS data
    st.subheader("Astronauts Currently in Space")
    astros = fetch_astros()
    if astros:
        number_in_space = astros['number']
        st.write(f"Number of people in space: {number_in_space}")
        astronaut_data = [{"Name": person['name'], "Craft": person['craft']} for person in astros['people']]
        df = pd.DataFrame(astronaut_data)
        st.table(df)
    else:
        st.error("Failed to retrieve astronaut data.")

    # Refresh data button at the bottom
    if st.button("Refresh Data"):
        st.experimental_rerun()

if __name__ == "__main__":
    main()
