import json 
import psycopg2 
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_weather():
    logging.info("Starting load process...")
    try:
        with open('raw_weather.json', 'r') as f:
            data = json.dumps(json.load(f))

        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB", "weather_db"), 
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "password"),
            host=os.getenv("POSTGRES_HOST", "localhost")
        )
        cur = conn.cursor()
        
        cur.execute("""
            CREATE SCHEMA IF NOT EXISTS raw;
            CREATE TABLE IF NOT EXISTS raw.open_meteo (
                id SERIAL PRIMARY KEY,
                payload JSONB,
                loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            INSERT INTO raw.open_meteo (payload) VALUES (%s);
        """, (data,))
        
        conn.commit()
        cur.close()
        conn.close()
        logging.info("Success: Data loaded to weather_db.")
        
    except Exception as e:
        logging.error(f"Load Error: {e}")
        raise

load_weather()