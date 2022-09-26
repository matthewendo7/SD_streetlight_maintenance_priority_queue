from uszipcode import SearchEngine, SimpleZipcode, ComprehensiveZipcode
import pandas as pd

search = SearchEngine()

# open the closed (no referral) reports and open reports
street_light_closed_no_refer = pd.read_csv('street_light_closed_no_refer.csv')
street_light_open = pd.read_csv('street_light_open.csv')

# 7980 closed entries with no or out of range zipcodes
closed_no_zip = street_light_closed_no_refer.loc[~street_light_closed_no_refer['zipcode'].between(91900, 92200)]
closed_no_zip.info(verbose = True)
# 19 open entries with no or out of range zipcodes
open_no_zip = street_light_open.loc[~street_light_open['zipcode'].between(91900, 92200)]

# 51 closed entries with no or out of range zipcodes and coordinates
closed_no_zip_no_coord = closed_no_zip.loc[~closed_no_zip['lat'].between(32, 33.5) | ~closed_no_zip['lng'].between(-118, -116)]
closed_no_zip_no_coord.info(verbose = True)
# 0 open entries with no or out of range zipcodes and coordinates
open_no_zip_no_coord = open_no_zip.loc[~closed_no_zip['lat'].between(32, 33.5) | ~open_no_zip['lng'].between(-118, -116)]


# take the open reports that are missing zip codes and utilize the coordinate data to determine zip code. add zip codes to dataframe. export to csv
# uszipcode package is difficult to work with pandas dataframe, should look into more concise code for this operation later
open_lats = open_no_zip['lat'].to_list()
open_lngs = open_no_zip['lng'].to_list()
open_zipcodes = []
open_pop_density = []
for i in range(len(open_lats)):
    result = search.by_coordinates(lat = open_lats[i], lng = open_lngs[i], radius = 50, returns = 1)
    open_zipcodes.append(result[0].zipcode)

street_light_open.loc[~street_light_open['zipcode'].between(91900, 92200), 'zipcode'] = open_zipcodes

street_light_open.to_csv('street_light_open_zip_added.csv', index=False)


# removed entries that don't contain zip code and coordinate data
# take the closed (no referral) reports that are missing zip codes and utilize the coordinate data to determine zip code. add zip codes to dataframe. export to csv
# uszipcode package is difficult to work with pandas dataframe, should look into more concise code for this operation later
street_light_closed_no_refer = street_light_closed_no_refer[(street_light_closed_no_refer['zipcode'].between(91900, 92200)) | ((street_light_closed_no_refer['lat'].between(32, 33.5)) & (street_light_closed_no_refer['lng'].between(-118, -116)))]
closed_no_zip = street_light_closed_no_refer.loc[~street_light_closed_no_refer['zipcode'].between(91900, 92200)]

closed_lats = closed_no_zip['lat'].to_list()
closed_lngs = closed_no_zip['lng'].to_list()
closed_zipcodes = []
for i in range(len(closed_lats)):
    result = search.by_coordinates(lat = closed_lats[i], lng = closed_lngs[i], radius = 50, returns = 1)
    closed_zipcodes.append(result[0].zipcode)

street_light_closed_no_refer.loc[~street_light_closed_no_refer['zipcode'].between(91900, 92200), 'zipcode'] = closed_zipcodes

street_light_closed_no_refer.to_csv('street_light_closed_no_refer_zip_added.csv', index=False)
