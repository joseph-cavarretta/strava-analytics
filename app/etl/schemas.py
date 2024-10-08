raw_cols = [
    'id', 
    'name', 
    'start_date', 
    'start_date_local', 
    'type', 
    'distance', 
    'distance_units', 
    'moving_time', 
    'elapsed_time', 
    'time_units', 
    'total_elevation_gain', 
    'elevation_units'
]

processed_cols = [
    'id', 
    'name', 
    'type', 
    'miles', 
    'moving_time_sec', 
    'elapsed_time_sec', 
    'hours',
    'elevation_gain_ft', 
    'start_date', 
    'start_date_local',
    'date', 
    'year', 
    'month', 
    'day_of_month', 
    'week_of_year', 
    'day_of_year',
    'year_week',
    'route1_name', 
    'route1_count', 
    'route2_name',
    'route2_count', 
    'route3_name',
    'route3_count',
    'label',
    'type_id',
    'date_id',
    'activity_id',
    'type_name'
]

activity_cols = [
    'id',
    'date_id',
    'type_id',
    'name',
    'miles',
    'hours',
    'moving_time_sec',
    'elapsed_time_sec',
    'elevation_gain_ft',
    'start_date_local'
]

date_cols = [
    'date_id',
    'year',
    'month',
    'day_of_month',
    'week_of_year',
    'day_of_year',
    'year_week'
]

type_cols = [
    'type_id',
    'type_name',
    'label'
]

counts_cols = [
    'activity_id',
    'route1_name',
    'route1_count',
    'route2_name',
    'route2_count',
    'route3_name',
    'route3_count'
]

type_labels = {
    'aerobic': [
        'Run',
        'Ride',
        'BackcountrySki',
        'NordicSki',
        'Swim',
        'Elliptical'
    ],
    'non-aerobic': [
        'AlpineSki', 
        'WeightTraining', 
        'Workout', 
        'RockClimbing', 
        'Pickleball'
    ],
    'omit': [
        'AlpineSki', 
        'Walk'
    ]
}