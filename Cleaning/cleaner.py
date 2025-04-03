import csv
from collections import Counter, defaultdict

#fix missing age without 3rd party libraries

def read_csv(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        header = lines[0].strip().split(',')
        data = [line.strip().split(',') for line in lines[1:]]
        return header, data

fact_csv = read_csv('../../datasets/test.csv')

#print(fact_csv[0])


def fix_age(data):
    #get a dictionary and store the age of each player
    age_data = defaultdict(list)

    for row in data:
        
        print("Row Data ----?"  , row)
        player_id = row[1]
        # Collect AGE data
        if row[8] not in ['UNKNOWN', 'N/A', '', None]:
            try:
                print("Age is -- " ,row[8])
                age_data[1].append(float(row[8]))
            except ValueError:
                pass
    
    # Calculate the average age for each player
    average_age = {player_id: sum(ages) / len(ages) for player_id, ages in age_data.items()}

    # Replace 'UNKNOWN' with the average age for each player
    for row in data:
        player_id = row[1]
        if row[8] == 'UNKNOWN':
            row[8] = average_age.get(player_id, 'UNKNOWN')
        elif row[8] == 'N/A':

            row[8] = average_age.get(player_id, 'N/A')
        elif row[8] == '':
            row[8] = average_age.get(player_id, '')
        elif row[8] == None:
            row[8] = average_age.get(player_id, None)
        else:
            row[8] = row[8]
    return data 


def write_csv(file_path, header, data):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for row in data:
            writer.writerow(row.values())   


tes2 =  fix_age(fact_csv[1])
write_csv('../../datasets/test2.csv', tes2[0], tes2[1])


    
