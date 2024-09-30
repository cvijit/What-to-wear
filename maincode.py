import streamlit as st
import requests

# OpenWeatherMap API key (replace with your own)
API_KEY = "9e3af6fd34f4c9917dd80311f7d75a40"

# Mapping Dublin areas to their coordinates for API calls
DUBLIN_AREAS = {
    "Dublin 1": {"lat": 53.348, "lon": -6.2603},
    "Dublin 2": {"lat": 53.3382, "lon": -6.2556},
    "Dublin 3": {"lat": 53.3709, "lon": -6.2285},
    "Dublin 4": {"lat": 53.326, "lon": -6.2224},
    "Dublin 5": {"lat": 53.3881, "lon": -6.1887},
    # Add more areas as needed
}

# Function to fetch live weather data
def get_weather_data(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to retrieve weather data")
        return None

# Function to suggest outfit based on weather conditions
def suggest_outfit(temp, weather, gender):
    outfit = ""
    
    if gender == "Male":
        if temp > 20:
            outfit = "T-shirt, shorts, and sunglasses."
        elif 10 < temp <= 20:
            outfit = "Light jacket, jeans, and sneakers."
        elif temp <= 10:
            outfit = "Warm coat, scarf, and boots."
        if "rain" in weather.lower():
            outfit += " Don't forget a raincoat or umbrella!"
    elif gender == "Female":
        if temp > 20:
            outfit = "Dress or light top, shorts, and sunglasses."
        elif 10 < temp <= 20:
            outfit = "Light jacket, jeans, and comfortable shoes."
        elif temp <= 10:
            outfit = "Warm coat, scarf, and boots."
        if "rain" in weather.lower():
            outfit += " Don't forget an umbrella!"
    
    return outfit

# Streamlit App Layout
st.title("Dublin Outfit Suggestion Based on Live Weather")

# Choose the Dublin area
area = st.selectbox("Select your area in Dublin", list(DUBLIN_AREAS.keys()))

# Choose gender
gender = st.selectbox("Select your gender", ["Male", "Female"])

# Fetch weather data
if area:
    st.write(f"Fetching weather data for {area}...")
    coordinates = DUBLIN_AREAS[area]
    weather_data = get_weather_data(coordinates["lat"], coordinates["lon"])

    if weather_data:
        temp = weather_data['main']['temp']
        weather_condition = weather_data['weather'][0]['description']

        # Display the weather details
        st.subheader(f"Weather in {area}:")
        st.write(f"Temperature: {temp}°C")
        st.write(f"Condition: {weather_condition.capitalize()}")

        # Suggest an outfit based on weather and gender
        outfit = suggest_outfit(temp, weather_condition, gender)
        st.subheader("Suggested Outfit:")
        st.write(outfit)
