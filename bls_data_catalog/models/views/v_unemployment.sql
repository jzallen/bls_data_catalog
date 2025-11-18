{{
  config(
    materialized='view',
    meta={
      'access_level': 'public',
      'description': 'Public interface for unemployment data with state metadata'
    }
  )
}}

-- VIEWS LAYER - v_unemployment
-- Public interface that joins unemployment rates with state metadata
-- This view enforces data quality and provides a clean API for downstream reports

with unemployment as (
    select
        state_fips,
        year_month::date as year_month,
        unemployment_rate,
        labor_force,
        unemployed,
        series_id
    from {{ source('bls_raw', 'unemployment_monthly') }}
    where unemployment_rate >= 0
        and labor_force > 0
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
    u.state_fips,
    s.state_name,
    s.state_abbr,
    s.region_name,
    s.division_name,
    u.year_month,
    extract(year from u.year_month) as year,
    extract(month from u.year_month) as month,
    date_trunc('quarter', u.year_month) as year_quarter,
    u.unemployment_rate,
    u.labor_force,
    u.unemployed,
    u.series_id
from unemployment u
inner join states s
    on u.state_fips = s.state_fips
