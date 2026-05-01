# 🌤️ Weather Data Pipeline (ETL + dbt)

## Overview
End-to-end data pipeline yang mengambil data cuaca Jakarta dari **Open-Meteo API**, menyimpannya ke **PostgreSQL**, dan mentransformasinya menggunakan **dbt** menjadi data mart siap analisis.

**Problem:** Data cuaca mentah dari API tidak terstruktur dan sulit dianalisis langsung.  
**Solution:** Pipeline otomatis yang membersihkan dan mengagregasi data harian secara konsisten.

---

## Architecture
```
Open-Meteo API → Python ETL → PostgreSQL (raw) → dbt (staging → mart)
```

---

## Tech Stack
| Tool | Fungsi |
|------|--------|
| Python | Extract & Load data dari API ke PostgreSQL |
| PostgreSQL | Raw data storage (format JSONB) |
| dbt | Data transformation, testing & dokumentasi |

---

## Pipeline Flow

### 1. Extract
- Fetch data cuaca harian Jakarta dari Open-Meteo API
- Parameter: `temperature_2m_max`, `temperature_2m_min`, `precipitation_sum`
- Koordinat: Jakarta (-6.2, 106.8)

### 2. Load
- Simpan raw response ke PostgreSQL schema `raw` dalam format JSONB
- Append-only, data historis tetap terjaga

### 3. Transform (dbt)
```
raw.open_meteo_raw
    └── stg_open_meteo        # parsing JSON → structured columns, type casting
            └── daily_weather  # agregasi harian (avg, max, min temp, precipitation)
```

---

## dbt Models

### Staging — `stg_open_meteo`
- Parse JSONB → structured columns
- Rename & cast tipe data
- Handle NULL values

### Mart — `daily_weather`
- Agregasi suhu harian (avg, max, min)
- Total curah hujan per hari
- Siap untuk analisis & visualisasi

---

## Data Quality Tests
| Test | Kolom |
|------|-------|
| `not_null` | date, temperature_max, temperature_min |
| `unique` | date (di mart layer) |
| `accepted_values` | temperature range (-10 to 50°C) |

---

## Output Sample
| date | avg_temp | max_temp | min_temp |
|------|----------|----------|----------|
| 2026-04-30 | 26.51 | 31.4 | 23.6 |
| 2026-05-01 | 26.47 | 31.3 | 24.0 |
| 2026-05-02 | 26.07 | 29.6 | 23.4 |
| 2026-05-03 | 25.39 | 29.4 | 23.0 |
| 2026-05-04 | 25.92 | 29.5 | 24.0 |
| 2026-05-05 | 26.10 | 28.7 | 24.1 |
| 2026-05-06 | 27.24 | 30.2 | 24.9 |

---

## Key Insights
- Suhu rata-rata Jakarta berkisar antara **25-27°C**
- Suhu maksimum bisa mencapai **31°C** di siang hari
- Suhu minimum konsisten di sekitar **23-24°C** di malam hari
- Pipeline fetch **7 hari forecast** dari Open-Meteo API secara otomatis

---

## How to Run

```bash
# 1. Clone repository
git clone https://github.com/username/weather-pipeline.git
cd weather-pipeline

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup environment variables
cp .env.example .env
# Edit .env dengan kredensial PostgreSQL lo

# 4. Extract & Load
python extract.py
python load.py

# 5. Transform
dbt deps
dbt run
dbt test

# 6. Generate dokumentasi
dbt docs generate
dbt docs serve
```

---

## Project Structure
```
weather-pipeline/
├── extract.py              # Fetch data dari Open-Meteo API
├── load.py                 # Load raw data ke PostgreSQL
├── requirements.txt
├── .env.example
├── models/
│   ├── staging/
│   │   ├── stg_open_meteo.sql
│   │   └── schema.yml      # sources & tests
│   └── marts/
│       ├── daily_weather.sql
│       └── schema.yml      # tests & dokumentasi
├── dbt_project.yml
└── README.md
```

---

## What I Learned
- Membangun pipeline ETL end-to-end dari API ke data mart
- Implementasi data modeling dengan dbt (staging → mart pattern)
- Data quality testing otomatis dengan dbt tests
- Handling raw JSON data di PostgreSQL

