-- used to create a dataset in Apache Superset UI
SELECT 
  a.id, a.date_id, RTRIM(name) AS name, a.miles, a.hours, a.elevation_gain_ft, 
  d.year_week, d.week_of_year, d.year, d.month, d.day_of_month, d.day_of_year,
  t.type_name, t.label,
  c.route1_count AS bear_peak_count, c.route2_count AS sanitas_count, c.route3_count AS second_flatiron_count,
  ROUND(SUM(a.hours) OVER (PARTITION BY d.year ORDER BY a.date_id), 2) AS rolling_yearly_hrs,
  ROUND(SUM(a.miles) OVER (PARTITION BY d.year ORDER BY a.date_id), 2) AS rolling_yearly_mi,
  ROUND(SUM(a.elevation_gain_ft) OVER (PARTITION BY d.year ORDER BY a.date_id), 2) AS rolling_yearly_gain
FROM
  activities a
  JOIN dates d ON a.date_id=d.date_id
  JOIN types t ON a.type_id=t.type_id
  JOIN counts c ON a.id=c.activity_id
ORDER BY a.date_id DESC