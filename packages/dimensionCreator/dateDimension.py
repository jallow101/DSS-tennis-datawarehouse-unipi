import csv
from datetime import datetime

def create_date_dimension_from_tourney(data):
    unique_dates = set()
    
    # Step 1: Extract all unique tourney dates
    for row in data:
        timestamp = row.get('tourney_timestamp', '').strip()
        if timestamp:
            date_only = timestamp.split(' ')[0]
            unique_dates.add(date_only)

    # Step 2: Build date dimension
    date_dimension = []
    for idx, date_str in enumerate(sorted(unique_dates), start=1):
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            continue  # skip invalid date

        day = date_obj.day
        day_of_week = date_obj.strftime("%A")
        is_weekend = 1 if day_of_week in ['Saturday', 'Sunday'] else 0
        week = int(date_obj.strftime("%V"))  # ISO week number
        month = date_obj.month
        quarter = (month - 1) // 3 + 1
        year = date_obj.year

        date_dimension.append({
            'date_id': idx,
            'date': date_str,
            'day': day,
            'day_of_week': day_of_week,
            'is_weekend': is_weekend,
            'week': week,
            'month': month,
            'quarter': quarter,
            'year': year
        })

    return date_dimension