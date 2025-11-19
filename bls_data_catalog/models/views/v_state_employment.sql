{{
  config(
    materialized='view',
    meta={
      'access_level': 'public',
      'description': 'Combined view of employment and unemployment metrics'
    }
  )
}}

-- VIEWS LAYER - v_state_employment
-- Combines employment and unemployment data into a single comprehensive view
-- This is a 1:1 join on state and month

with employment as (
    select
        state_fips,
        state_name,
        state_abbr,
        region_name,
        division_name,
        year_month,
        year,
        month,
        year_quarter,
        employment_level
    from {{ ref('v_employment') }}
),

unemployment as (
    select
        state_fips,
        year_month,
        unemployment_rate,
        labor_force,
        unemployed
    from {{ ref('v_unemployment') }}
)

select
    e.state_fips,
    e.state_name,
    e.state_abbr,
    e.region_name,
    e.division_name,
    e.year_month,
    e.year,
    e.month,
    e.year_quarter,
    -- Raw BLS values (already in thousands)
    e.employment_level,  -- Employment level in thousands
    u.unemployment_rate,  -- Unemployment rate as percentage
    u.labor_force,  -- Labor force in thousands
    u.unemployed  -- Unemployed persons in thousands
from employment e
inner join unemployment u
    on e.state_fips = u.state_fips
    and e.year_month = u.year_month
