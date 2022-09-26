import pandas as pd
import numpy as np
import heapq
from math import nan, isnan

# open closed and open report data
street_light_closed = pd.read_csv('street_light_closed_no_refer_zip_pop_density_income_added.csv')
street_light_open = pd.read_csv('street_light_open_no_refer_zip_pop_density_income_added.csv')

# check if any null
# print(pd.isnull(street_light_open['population_density']).values.any())
# print(pd.isnull(street_light_open['household_income']).values.any())
# print(pd.isnull(street_light_closed['population_density']).values.any())
# print(pd.isnull(street_light_closed['household_income']).values.any())

# combine open and closed reports
street_light = pd.concat([street_light_closed, street_light_open])

# calculate the age of the requests
def calculate_days(entry_date):
    today = pd.Timestamp('today')
    return (today - entry_date).dt.days

street_light['request_age'] = calculate_days(pd.to_datetime(street_light['date_requested']))

# sanity check on factors
# print(street_light['request_age'].min(), street_light['request_age'].max())
# print(street_light['population_density'].min(), street_light['population_density'].max())
# print(street_light['household_income'].min(), street_light['household_income'].max())

# calculate priority scores for how old the request is 0 for oldest and 1 for most recent. lower priority score is higher priority in the queue
street_light['request_age_score'] = 1 - (street_light['request_age'] - street_light['request_age'].min()) / (street_light['request_age'].max() - street_light['request_age'].min())

# calculate priority scores for population density (foot traffic representative) is 0 for highest density and 1 for lowest density. lower priority score is higher priority in the queue
street_light['population_density_score'] = 1 - (street_light['population_density'] - street_light['population_density'].min()) / (street_light['population_density'].max() - street_light['population_density'].min())

# calculate priority scores for household income (crime rate representative) is 0 for lowest median household income and 1 for highest median household income. lower priority score is higher priority in the queue
street_light['household_income_score'] = (street_light['household_income'] - street_light['household_income'].min()) / (street_light['household_income'].max() - street_light['household_income'].min())

# sanity check as should be between 0 and 1
# print(street_light['request_age_score'].min(), street_light['request_age_score'].max())
# print(street_light['population_density_score'].min(), street_light['population_density_score'].max())
# print(street_light['household_income_score'].min(), street_light['household_income_score'].max())

# calculate total priority score where request age is 40% of the score, household income is 40%, and population density is 20%
street_light['priority_score'] = street_light['request_age_score'] + street_light['household_income_score'] + 0.5 * street_light['population_density_score']

# create priority queue
priority_queue = []
[heapq.heappush(priority_queue, (x, y)) for x, y in zip(street_light['priority_score'], street_light['service_request_id'])]



# calculate statistics if priority queue was implemented from the start
# get list of closed dates as those will be closed dates for priority queue
date_closed = street_light_closed['date_closed'].to_list()
date_closed = [x for x in date_closed if isinstance(x, str)]
date_closed.sort()
priority_closed_length = len(date_closed)
priority_date_closed = pd.DataFrame(date_closed)

# sort all of the reports (open and closed) by priority score and filter higher scored ones so number of reports are the same as the number that were closed
sorted_street_light = street_light.sort_values(by=['priority_score'])
priority_street_light = sorted_street_light.iloc[:priority_closed_length]

# add the request dates to date closed dataframe and calculate the difference to get how long the reports were open if the priority queue determined which reports to complete
priority_date_closed['date_requested'] = priority_street_light['date_requested'].to_list()
priority_date_closed.rename(columns={ priority_date_closed.columns[0]: "date_closed" }, inplace = True)
priority_date_closed['date_closed'] = priority_date_closed['date_closed'].astype('datetime64[ns]')
priority_date_closed['date_requested'] = priority_date_closed['date_requested'].astype('datetime64[ns]')
priority_date_closed['Difference'] = priority_date_closed['date_closed'].sub(priority_date_closed['date_requested'], axis=0).dt.days

# for reports chosen by priority queue, calculate average and median for how long reports were open, the population density score, and household income score 
print(priority_date_closed['Difference'].mean())
print(priority_date_closed['Difference'].median())

print(priority_street_light['population_density_score'].mean())
print(priority_street_light['population_density_score'].median())

print(priority_street_light['household_income_score'].mean())
print(priority_street_light['household_income_score'].median())


# for the actual closed reports, calculate average and median for how long reports were open, the population density score, and household income score 
print(street_light[street_light['status'] == 'Closed']['population_density_score'].mean())
print(street_light[street_light['status'] == 'Closed']['population_density_score'].median())

print(street_light[street_light['status'] == 'Closed']['household_income_score'].mean())
print(street_light[street_light['status'] == 'Closed']['household_income_score'].median())



