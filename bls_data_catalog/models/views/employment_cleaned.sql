{{
  config(
    materialized='view',
    meta={
      'access_level': 'public',
      'description': 'Public interface for employment data with state metadata'
    }
  )
}}

-- VIEWS LAYER - employment_cleaned
-- Public interface that joins employment levels with state metadata
-- This view enforces data quality and provides a clean API for downstream reports

with employment as (
    select
        state_fips,
        year_month::date as year_month,
        employment_level,
        series_id
    from {{ source('bls_raw', 'employment_monthly') }}
    where employment_level > 0
),

states as (
    select
        state_fips,
        state_name,
        state_abbr,
        region_name,
        division_name
    from {{ source('bls_raw', 'states') }}
)

select
    e.state_fips,
    s.state_name,
    s.state_abbr,
    s.region_name,
    s.division_name,
    e.year_month,
    extract(year from e.year_month) as year,
    extract(month from e.year_month) as month,
    date_trunc('quarter', e.year_month) as year_quarter,
    e.employment_level,
    e.series_id
from employment e
inner join states s
    on e.state_fips = s.state_fips
