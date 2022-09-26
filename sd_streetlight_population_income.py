from encodings import search_function
from uszipcode import SearchEngine
import pandas as pd
import numpy as np


# open open and closed reports where zip code are added
street_light_closed = pd.read_csv('street_light_closed_no_refer_zip_added.csv')
street_light_open = pd.read_csv('street_light_open_zip_added.csv')

# closed cases were closed after 152 days on average with 89 days being the median
# print(street_light_closed['case_age_days'].mean())
# print(street_light_closed['case_age_days'].median())

def calculate_days(date):
    today = pd.Timestamp('2022-09-22')
    return (today - date).dt.days


days_open = calculate_days(pd.to_datetime(street_light_open['date_requested']))

# open cases have been opened on average for 332 days with 272 days being the median
# print(days_open.mean())
# print(days_open.median())


# convert zip codes for open and closed reports and create dataframe
open_zipcodes = street_light_open['zipcode'].to_list()
closed_zipcodes = street_light_closed['zipcode'].to_list()
open_zipcodes = [int(item) for item in open_zipcodes]
closed_zipcodes = [int(item) for item in closed_zipcodes]

open_zipcodes = pd.DataFrame({'zipcodes': open_zipcodes})
closed_zipcodes = pd.DataFrame({'zipcodes': closed_zipcodes})

# initiate lists for the population density (in lieu of foot traffic) and household income (in lieu of crime rate) for open and closed reports
open_pop_density = []
open_household_income = []
closed_pop_density = []
closed_household_income = []

# utilize uszipcode package to acquire 2010 US census data based on zip code
# uszipcode package is difficult to work with pandas dataframe, should look into more concise code for this operation later
search = SearchEngine()
for i in np.arange(0, len(open_zipcodes['zipcodes'])):
    zipcode = search.by_zipcode(open_zipcodes['zipcodes'][i])
    if not zipcode.population:
        # Checking for non std zipcodes like postal boxes
        res = search.by_city_and_state(city=zipcode.major_city, state=zipcode.state)
        if (len(res)) > 0:
            zipcode = res[0]
    open_pop_density.append(zipcode.population_density)
    open_household_income.append(zipcode.median_household_income)

for i in np.arange(0, len(closed_zipcodes['zipcodes'])):
    zipcode = search.by_zipcode(closed_zipcodes['zipcodes'][i])
    if not zipcode.population:
        # Checking for non std zipcodes like postal boxes
        res = search.by_city_and_state(city=zipcode.major_city, state=zipcode.state)
        if (len(res)) > 0:
            zipcode = res[0]
    closed_pop_density.append(zipcode.population_density)
    closed_household_income.append(zipcode.median_household_income)

# add 2010 Census population density and household income data to dataframe
street_light_open['population_density'] = open_pop_density
street_light_open['household_income'] = open_household_income
street_light_closed['population_density'] = closed_pop_density
street_light_closed['household_income'] = closed_household_income

# export to csv
street_light_open.to_csv('street_light_open_no_refer_zip_pop_density_income_added.csv', index=False)
street_light_closed.to_csv('street_light_closed_no_refer_zip_pop_density_income_added.csv', index=False)