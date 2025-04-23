import sys
sys.path.append("../packages/main/")  # Ensure the path is correct
from main import read_csv, write_csv, drop_columns, convert_xml_to_csv, convert_json_to_csv
sys.path.append("../packages/factCleaner/")  # Ensure the path is correct
from factCleaner import fix_age_height_country
from handRankCleaner import fix_hand_and_rankpoints, fix_rank_by_tourney
sys.path.append("../packages/tourneyCleaner/")  # Ensure the path is correct
from tourneyFunctions import fix_surface, fix_draw_size


#convert other datasets to csv
convert_xml_to_csv('../datasets/countries.xml')
convert_json_to_csv('../datasets/tourney.json')
        
data, header = read_csv('../datasets/fact.csv')

#colmns with more that 70% missing values.. 
cols_to_remove = ['winner_entry', 'loser_seed', 'minutes', 'w_SvGms', 'l_SvGms',
                   'w_1stWon', 'l_ace', 'w_2ndWon', 'w_1stIn', 'w_svpt', 'w_df',
                   'w_bpSaved', 'w_bpFaced', 'l_svpt', 'l_1stIn', 'l_1stWon',
                   'l_2ndWon', 'l_bpSaved', 'l_bpFaced', 'w_ace', 'l_df',
                   'loser_entry', 'winner_seed']

fact_csv, updated_headers = drop_columns(data, cols_to_remove)

clean_v1 = fix_age_height_country(fact_csv)
print("...... Age and Height Imputation Done !!!! . .. ... .. .. .. .. .. .. .. .. ..")

clean_v2= fix_hand_and_rankpoints(clean_v1)
print("...... Hand an RankPoints Imputation Done !!!! . .. ... .. .. .. .. .. .. .. .. ..")

clean_v3 = fix_rank_by_tourney(clean_v2)
print("...... Player Rank Imputation Done !!!! . .. ... .. .. .. .. .. .. .. .. ..")

#print("Data ----?"  , clean_v2)
print("...... la Laa Laaaaaaaaa !!!! . .. ... .. .. .. .. .. .. .. .. ..")
write_csv('../datasets/cleaned/fact.csv', updated_headers, clean_v3)


print(". !!!! Aspertaaaaa lets fix the tourney dataset quick... .. .. .. .. .. .. .. .. ..")
tourney_data, tourney_header = read_csv('./tourney.csv') #chnage later and use datatset file
print("...... Tourney Dataset Loaded !!!! . .. ... .. .. .. .. .. .. .. .. ..")

clean_tourney_v1 = fix_surface(tourney_data)

clean_tourney_v2 = fix_draw_size(clean_tourney_v1)
print("...... Tourney Dataset Cleaned !!!! . .. ... .. .. .. .. .. .. .. .. ..")

write_csv('../datasets/cleaned/tourney.csv', tourney_header, clean_tourney_v2)

