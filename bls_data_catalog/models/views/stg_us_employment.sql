{{
  config(
    materialized = 'view'
  )
}}

-- Staging model for US employment data
-- Source: datahub.io/core/employment-us
-- Data spans 1941-2010 with annual employment statistics

select
    nation,
    -- Keep original year as integer for categorical dimension
    year as year_number,
    -- Convert year to date for MetricFlow time dimension
    cast(year || '-01-01' as date) as year,
    population,
    labor_force,
    population_percent as labor_force_participation_rate,
    employed_total,
    employed_percent as employment_population_ratio,
    agrictulture_ratio as employed_agriculture,
    nonagriculture_ratio as employed_nonagriculture,
    unemployed,
    unemployed_percent as unemployment_rate,
    not_in_labor as not_in_labor_force,
    footnotes
from {{ ref('us_employment') }}
