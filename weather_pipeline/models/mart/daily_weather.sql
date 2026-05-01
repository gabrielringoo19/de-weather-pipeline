select
    date(time) as date,
    avg(temperature) as avg_temperature,
    max(temperature) as max_temperature,
    min(temperature) as min_temperature
from {{ ref('stg_open_meteo') }}
group by date(time)
