import requests


def get_temperature(city):
    # Define the URL for the weather service
    url = f"https://wttr.in/{city}?format=%t"
    
    # Send a request to the wttr.in service
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        temperature = response.text.strip()
        temperature = temperature.replace('C','Celsius')
        
        
        print(f"The current temperature in {city} is {temperature}")
        return(f"The current temperature in {city} is {temperature}")
    else:
        print("Error: Could not retrieve weather data. Please check the city name.")
        return("Error: Could not retrieve weather data. Please check the city name.")

