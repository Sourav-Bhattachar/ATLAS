from RUN.FEATURES.remove_words import remove_words
import requests

def country_details(query):
    words_to_remove = ['atlas','please','what','is','the','country','details','of','are','show','see']
    query = remove_words(query, words_to_remove)
    query = query.replace(' ','')
    query = str(query)
    x = query

    url = f"https://restcountries.com/v3.1/name/{x}?fullText=true"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            country_data = response.json()[0]
            response_text = (
                f'Country Name: {country_data.get("name", {}).get("common", "N/A")}.\n'
                f'Official Name: {country_data.get("name", {}).get("official", "N/A")}.\n'
                f'Capital: {country_data.get("capital", ["N/A"])[0]}.\n'
                f'Region: {country_data.get("region", "N/A")}.\n'
                f'Subregion: {country_data.get("subregion", "N/A")}.\n'
                f'Population: {country_data.get("population", "N/A")}.\n'
                f'Area: {country_data.get("area", "N/A")} square kilo meters.\n'
                f'Languages: {list(country_data.get("languages", {}).values())}.\n'
                f'Currencies: {[currency["name"] for currency in country_data.get("currencies", {}).values()]}.\n'
                f'Borders: {country_data.get("borders", [])}.'
            )
            print(response_text)
            flag_url = country_data.get("flags", {}).get("png", "N/A")
            return response_text, flag_url
        else:
            return "Country not found.", None
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return f"{query} is not a country name", None