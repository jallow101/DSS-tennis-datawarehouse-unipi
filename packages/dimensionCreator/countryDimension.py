def create_country_dimension(data):
    country_dim = []

    for row in data:
        country_dim.append({
            'country_id': row.get('country_code', '').strip(),
            'country_name': row.get('country_name', '').strip(),
            'continent': row.get('continent', '').strip()
        })

    # Add unknown country manually
    country_dim.append({
        'country_id': 'UNKNW',
        'country_name': 'Unknown',
        'continent': 'Unknown'
    })

    return country_dim
