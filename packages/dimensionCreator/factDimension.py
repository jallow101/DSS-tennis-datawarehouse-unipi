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

        #get winner and losser rank points
        wplayer_rank_points = row.get('winner_rank_points', '').strip()
        lplayer_rank_points = row.get('loser_rank_points', '').strip()

        wplayer_rank = row.get('winner_rank', '').strip()
        lplayer_rank = row.get('loser_rank', '').strip()
        
        
        round_number = row.get('round', '').strip()
        score = row.get('score', '').strip()
        best_of = row.get('best_of', '').strip()

        transformed_row = {
            'match_id': match_id,
            'tourney_id': tourney_id,
            'winner_id': wplayer_id,
            'loser_id': lplayer_id,
            'no_spectators': int(float(no_spectators)) ,
            'avg_ticket': round(float(avg_ticket), 2) if avg_ticket else 0.00,
            'match_expense': round(float(match_expense), 2) if match_expense else 0.00,
            'winner_rank_points': int(float(wplayer_rank_points)) if wplayer_rank_points else 0,
            'loser_rank_points': int(float(lplayer_rank_points)) if lplayer_rank_points else 0,
            'winner_rank': int(float(wplayer_rank)) if wplayer_rank else 0,
            'loser_rank': int(float(lplayer_rank)) if lplayer_rank else 0,
            'round': round_number,
            'score': score,
            'best_of': best_of
        }

        transformed_data.append(transformed_row)

    return transformed_data
