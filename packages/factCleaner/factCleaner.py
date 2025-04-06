from collections import defaultdict, Counter

def fix_age_height_country(data):
    INVALID_VALS = {'', 'N/A', 'UNKNOWN', None}

    # One dict per player_id for each feature
    age_data = defaultdict(list)
    height_data = defaultdict(list)
    ioc_data = defaultdict(list)

    # Step 1: Collect valid values across all players
    for row in data:
        for role in ['winner', 'loser']:
            pid = row.get(f'{role}_id', '').strip()

            # Age
            age_val = row.get(f'{role}_age', '').strip()
            if age_val and age_val not in INVALID_VALS:
                try:
                    age_data[pid].append(float(age_val))
                except ValueError:
                    continue

            # Height
            ht_val = row.get(f'{role}_ht', '').strip()
            if ht_val and ht_val not in INVALID_VALS:
                try:
                    height_data[pid].append(float(ht_val))
                except ValueError:
                    continue

            # IOC (country)
            ioc_val = row.get(f'{role}_ioc', '').strip()
            if ioc_val and ioc_val not in INVALID_VALS:
                ioc_data[pid].append(ioc_val)

    # Step 2: Compute imputation values
    avg_age = {pid: round(sum(vals) / len(vals)) for pid, vals in age_data.items()}
    avg_height = {pid: round(sum(vals) / len(vals)) for pid, vals in height_data.items()}
    most_common_ioc = {pid: Counter(vals).most_common(1)[0][0] for pid, vals in ioc_data.items()}

    # Step 3: Impute missing values
    for row in data:
        for role in ['winner', 'loser']:
            pid = row.get(f'{role}_id', '').strip()

            # Age
            age_val = row.get(f'{role}_age', '').strip()
            if not age_val or age_val in INVALID_VALS:
                row[f'{role}_age'] = int(avg_age.get(pid, 0))
            else:
                try:
                    row[f'{role}_age'] = int(round(float(age_val)))
                except ValueError:
                    row[f'{role}_age'] = int(avg_age.get(pid, 0))

            # Height
            ht_val = row.get(f'{role}_ht', '').strip()
            if not ht_val or ht_val in INVALID_VALS:
                row[f'{role}_ht'] = int(avg_height.get(pid, 0))
            else:
                try:
                    row[f'{role}_ht'] = int(round(float(ht_val)))
                except ValueError:
                    row[f'{role}_ht'] = int(avg_height.get(pid, 0))

            # IOC
            ioc_val = row.get(f'{role}_ioc', '').strip()
            if not ioc_val or ioc_val in INVALID_VALS:
                row[f'{role}_ioc'] = most_common_ioc.get(pid, 'UNK')

    return data
