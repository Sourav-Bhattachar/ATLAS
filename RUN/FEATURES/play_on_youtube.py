import webbrowser
import pywhatkit


def search_youtube(query):
    query = query.replace("play", "").replace("on youtube", "").strip()
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
    pywhatkit.playonyt(query)
    return f"This is what I found for your search!"
