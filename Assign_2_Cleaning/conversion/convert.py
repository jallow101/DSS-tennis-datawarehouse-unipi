#read file and convert to csv
import csv
import json
import xml.etree.ElementTree as ET
import datetime


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
                

convert_xml_to_csv('../../datasets/countries.xml')
convert_json_to_csv('../../datasets/sample_tourney.json')