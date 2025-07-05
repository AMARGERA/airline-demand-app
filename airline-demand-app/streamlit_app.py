import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Airline Market Demand", layout="wide")

st.title("✈️ Airline Booking Demand Insights")
st.markdown("Powered by AviationStack API")

# 🚨 Replace with your real API key below
api_key = "0c291d0cc2291af1631ad74ef57ffd38"

# Call AviationStack API
url = f"http://api.aviationstack.com/v1/flights?access_key={api_key}&limit=10"

response = requests.get(url)

if response.status_code == 200:
    api_data = response.json()
    flights = api_data.get("data", [])

    # Extract relevant data
    records = []
    for flight in flights:
        departure = flight.get("departure", {}).get("airport", "N/A")
        arrival = flight.get("arrival", {}).get("airport", "N/A")
        airline = flight.get("airline", {}).get("name", "N/A")
        status = flight.get("flight_status", "N/A")
        date = flight.get("departure", {}).get("scheduled", "N/A")

        records.append({
            "Airline": airline,
            "From": departure,
            "To": arrival,
            "Status": status,
            "Date": date
        })

    df = pd.DataFrame(records)

    # Filters
    route_filter = st.multiselect("Filter by Airline:", options=df["Airline"].unique(), default=df["Airline"].unique())
    filtered_df = df[df["Airline"].isin(route_filter)]

    # Display
    st.subheader("📊 Live Flight Data")
    st.dataframe(filtered_df)

else:
    st.error("Failed to fetch data from API. Please check your key or try again later.")
