{{
    config(
        materialized='table'
    )
}}

with source_data as (
    select
        fetch_timestamp,
        protocol_id,
        protocol_name,
        json_value(safe.parse_json(raw_json), '$.category') as category,
        json_value(safe.parse_json(raw_json), '$.chain') as main_chain,
        json_value(safe.parse_json(raw_json), '$.symbol') as token_symbol,
        safe_cast(json_value(safe.parse_json(raw_json), '$.tvl') as float64) as current_tvl,
        raw_json,
        -- Исправлена опечатка в row_number()
        row_number() over (partition by protocol_id order by fetch_timestamp desc) as rn
    from {{ source('bronze', 'bronze_protocols_raw') }}
)

select
    fetch_timestamp,
    protocol_id,
    coalesce(protocol_name, 'Unknown') as protocol_name,
    coalesce(category, 'Uncategorized') as category,
    coalesce(main_chain, 'Multi') as main_chain,
    token_symbol,
    coalesce(current_tvl, 0.0) as current_tvl
from source_data
where rn = 1
