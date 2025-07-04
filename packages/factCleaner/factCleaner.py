from collections import defaultdict, Counter

def fix_age_height_country(data): #time aware imputation --  we need to check the match_id and impute the age, height and country based on the match_id
    INVALID_VALS = {'', 'N/A', 'UNKNOWN', None}

    age_by_match = defaultdict(list)    # player_id -> list of (match_id, age)
    height_data = defaultdict(list)
    ioc_data = defaultdict(list)

    # Step 1: Collect valid values
    for row in data:
        match_id = row.get('match_id', '').strip()
        if not match_id or match_id in INVALID_VALS:
            continue
        try:
            match_id = int(match_id)
        except ValueError:
            continue

        for role in ['winner', 'loser']:
            pid = row.get(f'{role}_id', '').strip()

            # Age
            age_val = row.get(f'{role}_age', '').strip()
            if age_val and age_val not in INVALID_VALS:
                try:
                    age = float(age_val)
                    age_by_match[pid].append((match_id, age))
                except ValueError:
                    continue

            # Height
            ht_val = row.get(f'{role}_ht', '').strip()
            if ht_val and ht_val not in INVALID_VALS:
                try:
                    height_data[pid].append(float(ht_val))
                except ValueError:
                    continue

            # Country
            ioc_val = row.get(f'{role}_ioc', '').strip()
            if ioc_val and ioc_val not in INVALID_VALS:
                ioc_data[pid].append(ioc_val)

    # Step 2: Sort age data by match_id
    for pid in age_by_match:
        age_by_match[pid].sort()

    avg_height = {
        pid: round(sum(vals) / len(vals)) for pid, vals in height_data.items()
    }

    most_common_ioc = {
        pid: Counter(vals).most_common(1)[0][0] for pid, vals in ioc_data.items()
    }

    # Step 3: Impute values
    for row in data:
        match_id = row.get('match_id', '').strip()
        try:
            match_id = int(match_id)
        except (ValueError, TypeError):
            match_id = -1  # fallback

        for role in ['winner', 'loser']:
            pid = row.get(f'{role}_id', '').strip()

            # Age imputation
            age_val = row.get(f'{role}_age', '').strip()
            imputed_age = None

            if not age_val or age_val in INVALID_VALS:
                timeline = age_by_match.get(pid, [])
                before = [age for mid, age in timeline if mid <= match_id]
                after = [age for mid, age in timeline if mid > match_id]

                if before:
                    imputed_age = int(round(before[-1]))  # most recent before
                elif after:
                    imputed_age = int(round(after[0]))   # earliest after
                elif timeline:
                    max_age = max(age for _, age in timeline)
                    imputed_age = int(round(max_age))
                else:
                    imputed_age = 18  # fallback

                row[f'{role}_age'] = imputed_age
            else:
                try:
                    row[f'{role}_age'] = int(round(float(age_val)))
                except ValueError:
                    row[f'{role}_age'] = 18

            # Height imputation
            ht_val = row.get(f'{role}_ht', '').strip()
            if not ht_val or ht_val in INVALID_VALS:
                row[f'{role}_ht'] = int(avg_height.get(pid, 0))
            else:
                try:
                    row[f'{role}_ht'] = int(round(float(ht_val)))
                except ValueError:
                    row[f'{role}_ht'] = int(avg_height.get(pid, 0))

            # IOC imputation
            ioc_val = row.get(f'{role}_ioc', '').strip()
            if not ioc_val or ioc_val in INVALID_VALS:
                row[f'{role}_ioc'] = most_common_ioc.get(pid, 'UNK')

    return data
