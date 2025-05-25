import requests

def get_temperature(city):
    url = f"https://wttr.in/{city}?format=%t"
    response = requests.get(url)

    if response.status_code == 200:
        temperature = response.text.strip()
        temperature = temperature.replace('C','Celsius')
        print(f"The current temperature in {city} is {temperature}")
        return(f"The current temperature in {city} is {temperature}")
    else:
        print("Error: Could not retrieve weather data. Please check the city name.")
        return("Error: Could not retrieve weather data. Please check the city name.")
