def transform_fact(data): 
    transformed_data = []

    for row in data:
        match_number = row.get('match_num', '').strip()
        tourney_id = row.get('tourney', '').strip()

        match_id = match_number + '_' + tourney_id
        wplayer_id = row.get('winner_id', '').strip()
        lplayer_id = row.get('loser_id', '').strip()
        no_spectators = row.get('spectator', '').strip()
        avg_ticket = row.get('avg_ticket_price', '').strip()
        match_expense = row.get('match_expenses', '').strip()

        transformed_row = {
            'match_id': match_id,
            'tourney_id': tourney_id,
            'winner_id': wplayer_id,
            'loser_id': lplayer_id,
            'no_spectators': no_spectators,
            'avg_ticket': float(avg_ticket) if avg_ticket else 0.0,
            'match_expense': float(match_expense) if match_expense else 0.0,
        }

        transformed_data.append(transformed_row)

    return transformed_data
