from collections import defaultdict

def transform_tourney_dimension(data, date_dim):
    # Build date lookup from date_dim
    date_lookup = { row['date']: row['date_id'] for row in date_dim }

    seen = set()
    tourney_dim = []

    for row in data:
        tourney = row.get('tourney', '').strip()
        tid = row.get('tourney_id', '').strip()
        timestamp = row.get('tourney_timestamp', '').strip()
        date_str = timestamp.split(' ')[0] if timestamp else ''
        key = (tid, date_str)

        # Skip duplicates
        if key in seen:
            continue
        seen.add(key)

        tourney_dim.append({
            'tourney_id': tourney,
            'tourney_range': tid,
            'tourney_name': row.get('tourney_name', '').strip(),
            'surface': row.get('surface', '').strip(),
            'draw_size': row.get('draw_size', '').strip(),
            'tourney_level': row.get('tourney_level', '').strip(),
            'tourney_date_id': date_lookup.get(date_str, 0)
        })

    return tourney_dim
