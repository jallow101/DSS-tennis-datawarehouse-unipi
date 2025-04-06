from collections import defaultdict, Counter

def fix_hand_and_rankpoints(data):
    INVALID_VALS = {'', 'N/A', 'UNKNOWN', None}
    
    hand_data = defaultdict(list)       # player_id -> list of handedness values
    rankpt_data = defaultdict(list)     # player_id -> list of rank points

    # Step 1: Collect all valid data
    for row in data:
        for role in ['winner', 'loser']:
            pid = row.get(f'{role}_id', '').strip()

            # Collect handedness
            hand = row.get(f'{role}_hand', '').strip()
            if hand and hand not in INVALID_VALS:
                hand_data[pid].append(hand)

            # Collect rank points
            rank = row.get(f'{role}_rank_points', '').strip()
            if rank and rank not in INVALID_VALS:
                try:
                    rankpt_data[pid].append(float(rank))
                except ValueError:
                    continue

    # Step 2: Compute most common hand and average rank points per player
    most_common_hand = {
        pid: Counter(hands).most_common(1)[0][0] for pid, hands in hand_data.items()
    }

    average_rank_pts = {
        pid: round(sum(pts) / len(pts)) for pid, pts in rankpt_data.items()
    }

    # Step 3: Impute missing/invalid data
    for row in data:
        for role in ['winner', 'loser']:
            pid = row.get(f'{role}_id', '').strip()

            # Fix handedness
            hand_val = row.get(f'{role}_hand', '').strip()
            if not hand_val or hand_val in INVALID_VALS:
                row[f'{role}_hand'] = most_common_hand.get(pid, 'U')  # default 'U' if unknown

            # Fix rank points
            rank_val = row.get(f'{role}_rank_points', '').strip()
            if not rank_val or rank_val in INVALID_VALS:
                row[f'{role}_rank_points'] = int(average_rank_pts.get(pid, 0))
            else:
                try:
                    row[f'{role}_rank_points'] = int(round(float(rank_val)))
                except ValueError:
                    row[f'{role}_rank_points'] = int(average_rank_pts.get(pid, 0))

    return data


def fix_rank_by_tourney(data):
    INVALID_VALS = {'', 'N/A', 'UNKNOWN', None}

    # Store (player_id, tourney_id) -> [ranks]
    tourney_rank_data = defaultdict(list)
    # Store global player average as fallback
    global_rank_data = defaultdict(list)

    # Step 1: Collect valid rank data
    for row in data:
        tourney_id = row.get('tourney_id', '').strip()
        for role in ['winner', 'loser']:
            pid = row.get(f'{role}_id', '').strip()
            rank_val = row.get(f'{role}_rank', '').strip()
            if rank_val and rank_val not in INVALID_VALS:
                try:
                    rank = int(float(rank_val))
                    tourney_rank_data[(pid, tourney_id)].append(rank)
                    global_rank_data[pid].append(rank)
                except ValueError:
                    continue

    # Step 2: Compute average ranks
    avg_tourney_rank = {
        (pid, tid): round(sum(ranks) / len(ranks))
        for (pid, tid), ranks in tourney_rank_data.items()
    }

    avg_global_rank = {
        pid: round(sum(ranks) / len(ranks))
        for pid, ranks in global_rank_data.items()
    }

    # Step 3: Impute missing or invalid values
    for row in data:
        tourney_id = row.get('tourney_id', '').strip()
        for role in ['winner', 'loser']:
            pid = row.get(f'{role}_id', '').strip()
            key = (pid, tourney_id)
            rank_val = row.get(f'{role}_rank', '').strip()

            if not rank_val or rank_val in INVALID_VALS:
                row[f'{role}_rank'] = int(avg_tourney_rank.get(key,
                                        avg_global_rank.get(pid, 0)))
            else:
                try:
                    row[f'{role}_rank'] = int(round(float(rank_val)))
                except ValueError:
                    row[f'{role}_rank'] = int(avg_tourney_rank.get(key,
                                        avg_global_rank.get(pid, 0)))

    return data
