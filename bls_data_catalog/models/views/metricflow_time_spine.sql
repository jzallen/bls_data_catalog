{{
  config(
    materialized = 'table',
    schema = 'analytics'
  )
}}

-- MetricFlow time spine model
-- Required for semantic layer to work with time-based metrics
-- Covers the date range of our employment data (1941-2010)

WITH date_spine AS (
  SELECT
    CAST(d AS DATE) AS date_day
  FROM GENERATE_SERIES(
    CAST('1941-01-01' AS DATE),
    CAST('2010-12-31' AS DATE),
    INTERVAL '1 day'
  ) AS t(d)
)

SELECT
  date_day
FROM date_spine
