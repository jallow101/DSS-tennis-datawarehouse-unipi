from collections import defaultdict, Counter

def create_player_dim(data):
    player_info = defaultdict(lambda: {
        'names': set(),
        'hands': [],
        'ages': [],
        'heights': [],
        'iocs': [],
        #'rank_points': [],
        #'rank': []
    })

    for row in data:
        for role in ['winner', 'loser']:
            pid = row.get(f'{role}_id', '').strip()
            name = row.get(f'{role}_name', '').strip()
            hand = row.get(f'{role}_hand', '').strip()
            age = row.get(f'{role}_age', 0) or 0
            ht = row.get(f'{role}_ht', 0) or 0
            ioc = row.get(f'{role}_ioc', '').strip()
            #rank_points = row.get(f'{role}_rank_points', '').strip()
            #rank = row.get(f'{role}_rank', '').strip()

            if pid:
                if name:
                    player_info[pid]['names'].add(name)
                if hand:
                    player_info[pid]['hands'].append(hand)
                if age and str(age).isdigit():
                    player_info[pid]['ages'].append(int(age))
                if ht and str(ht).isdigit():
                    player_info[pid]['heights'].append(int(ht))
                if ioc:
                    player_info[pid]['iocs'].append(ioc)
                #if rank_points and str(rank_points).isdigit():
                #    player_info[pid]['rank_points'].append(int(rank_points))
                #if rank:
                #    player_info[pid]['rank'].append(rank)

    player_dim = []
    for pid, info in player_info.items():
        player_dim.append({
            'player_id': pid,
            'player_name': sorted(info['names'])[0] if info['names'] else 'Unknown',
            'hand': Counter(info['hands']).most_common(1)[0][0] if info['hands'] else 'U',
            'age': max(info['ages'] )if info['ages'] else 18,
            'height': round(sum(info['heights']) / len(info['heights'])) if info['heights'] else 0,
            'country_id': Counter(info['iocs']).most_common(1)[0][0] if info['iocs'] else 'UNKNW',
         #use in fact ---- #'rank_points': max(info['rank_points']) if info['rank_points'] else 0,
         #use in fact ---- #'rank': min(info['rank']) if info['rank'] else 9999
        })

    return player_dim
