import csv
import json
import xml.etree.ElementTree as ET
import datetime

def read_csv(file_path):
    data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)  # Automatically uses first row as keys
        for row in reader:
            data.append(row)

    return data, reader.fieldnames  # Return the data and the header


def write_csv(file_path, header, data):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for row in data:
           writer.writerow(row.values())   


def drop_columns(data, cols_to_remove):
    for row in data:
        headers = [key for key in row.keys() if key not in cols_to_remove]
        for col in cols_to_remove:
            #print(f"Removing column: {col} from row: {row}")
            row.pop(col, None)
            #print(f"Row after removal: {row}")
    return data, headers

#fucntion to convert file xml to csv
def convert_xml_to_csv(input_file,output_file='countries.csv'):
    rf = open(input_file, 'r')
    wf = open(output_file, 'w', newline='')
    writer = csv.writer(wf)
    writer.writerow(['country_code', 'country_name', 'continent'])

    tree = ET.parse(input_file)
    root = tree.getroot()
    
    #print(root.tag, "Root Element")

    for child in root:
        country_code = child.find('country_code').text
        country_name = child.find('country_name').text
        continent = child.find('continent').text
        writer.writerow([country_code, country_name, continent])

    rf.close()
    wf.close()


def convert_timestamp(ts):
    return datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc) + datetime.timedelta(seconds=ts)

#Convert JSON to CSV
def convert_json_to_csv(input_file, output_file='tourney.csv'):
   
    rf = open(input_file, 'r')
    data = json.load(rf)
    with open(output_file, 'w', newline='') as wf:
        writer = csv.writer(wf)
        writer.writerow(["tourney", "tourney_id","tourney_name","surface","draw_size","tourney_level","tourney_timestamp"])
        for item in data:
            if item == "data":
                for i in data[item]:
                    #print(type(i))
                    #print(i)
                    #print(i[0])
                    
                    #convert timestamp to datetime
                    ts = i[6]
                    converted_ts = convert_timestamp(ts)
                    writer.writerow([i[0], i[1], i[2], i[3], i[4], i[5], converted_ts]) 

    rf.close()
    wf.close()
                
