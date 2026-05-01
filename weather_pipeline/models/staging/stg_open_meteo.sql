select
    jsonb_array_elements_text(payload->'hourly'->'time') as time,
    (jsonb_array_elements(payload->'hourly'->'temperature_2m'))::float as temperature
from {{ source('raw', 'open_meteo') }}
