from collections import defaultdict, Counter

def fix_surface(data):
    surface_map = defaultdict(list)

    for row in data:
        name = row['tourney_name']
        surface = row['surface']
        if surface and surface != 'N/A':
            surface_map[name].append(surface)

    most_common_surface = {
        name: Counter(surfs).most_common(1)[0][0]
        for name, surfs in surface_map.items()
    }

    for row in data:
        if not row['surface'] or row['surface'] == 'N/A':
            row['surface'] = most_common_surface.get(row['tourney_name'], 'Hard')

    return data


def fix_draw_size(data):
    draw_map = defaultdict(list)

    for row in data:
        name = row['tourney_name']
        size = row['draw_size']
        if size and str(size).isdigit():
            draw_map[name].append(int(size))

    most_common_draw = {
        name: Counter(sizes).most_common(1)[0][0]
        for name, sizes in draw_map.items()
    }

    for row in data:
        size = row.get('draw_size', '')
        if not size or not str(size).isdigit():
            row['draw_size'] = most_common_draw.get(row['tourney_name'], 32)
        else:
            row['draw_size'] = int(size)

    return data
