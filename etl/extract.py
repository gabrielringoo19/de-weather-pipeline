import requests
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_weather(lat="-6.20", lon="106.81"):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"
    logging.info("Starting extraction...")
    
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        with open('raw_weather.json', 'w') as f:
            json.dump(res.json(), f)
        logging.info("Success: Data saved.")
    except requests.RequestException as e:
        logging.error(f"API Error: {e}")
        raise
    except Exception as e:
        logging.error(f"System Error: {e}")
        raise

extract_weather()