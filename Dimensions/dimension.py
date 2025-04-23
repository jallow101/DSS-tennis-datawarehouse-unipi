import sys
sys.path.append("../packages/main/")  # Ensure the path is correct
from main import read_csv, write_csv

sys.path.append("../packages/dimensionCreator/")  # Ensure the path is correct
from playerDimension import create_player_dim
from factDimension import transform_fact
from dateDimension import create_date_dimension_from_tourney
from tourneyDimension import transform_tourney_dimension
from countryDimension import create_country_dimension

fact_csv, header  = read_csv('../datasets/cleaned/fact.csv')
touney_csv, header  = read_csv('../datasets/cleaned/tourney.csv')
print("...... Fact & Tourney DatasetS Loaded !!!! . .. ... .. .. .. .. .. .. .. .. ..")

#####################################################################################
#                                                                                   #
#                  EXTRACT PLAYER DIMENSION TABLE FOR FACT DATASET                  #
#                                                                                   #
#####################################################################################
player_dim = create_player_dim(fact_csv)
write_csv('./dimension tables/player_dim.csv', player_dim[0].keys(), player_dim)
print("...... PLAYER Dimension Table Created !!!! . .. ... .. .. .. .. .. .. .. .. ..")
#####################################################################################
#                                                                                   #
#                TRANSFORM FACT DIMENSION TABLE FOR FACT DATASET                    #
#                                                                                   #
#####################################################################################
fact_dim = transform_fact(fact_csv)
write_csv('./dimension tables/fact_dim.csv', fact_dim[0].keys(), fact_dim)
print("...... Fact Dimension Table Created !!!! . .. ... .. .. .. .. .. .. .. .. ..")

#####################################################################################
#                                                                                   #
#                EXTRACT DATE DIMENSION TABLE FOR TOURNEY DATASET                   #
#                                                                                   #
#####################################################################################
#date_dim = create_date_dimension_from_tourney(touney_csv)   
#write_csv('./dimension tables/date_dim.csv', date_dim[0].keys(), date_dim)
#print("...... Date Dimension Table Created !!!! . .. ... .. .. .. .. .. .. .. .. ..")

#####################################################################################
#                                                                                   #
#                          TRANFROM TIMESTAMP to DATEID                             #         
#                                       AND                                         #
#              CREATE TOURNEY DIMENSION TABLE FOR TOURNEY DATASET                   #
#                                                                                   #
#####################################################################################

#tourney_dim = transform_tourney_dimension(touney_csv, date_dim)
#write_csv('./dimension tables/tourney_dim.csv', tourney_dim[0].keys(), tourney_dim)
#print("...... Tourney Dimension Table Created !!!! . .. ... .. .. .. .. .. .. .. .. ..")

#####################################################################################
#                                                                                   #
#                CREATE COUNTRY DIMENSION TABLE FOR COUNTRY DATASET                 #
#                                                                                   #
#####################################################################################

#country_csv, header  = read_csv('../datasets/cleaned/countries.csv')
#country_dim = create_country_dimension(country_csv)
#write_csv('./dimension tables/country_dim.csv', country_dim[0].keys(), country_dim)

