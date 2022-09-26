import pandas as pd

# open get it done open requests and filter for "Street Light Maintenance". export to csv
get_it_done_open = pd.read_csv('get_it_done_requests_open_datasd.csv')

street_light_open = get_it_done_open.loc[get_it_done_open['service_name'] == 'Street Light Maintenance']
street_light_open.to_csv('street_light_open.csv', index=False)

# open get it done closed requests and combine the all the requests from 2016-2022
get_it_done_2022 = pd.read_csv('get_it_done_requests_closed_2022_datasd.csv')
get_it_done_2021 = pd.read_csv('get_it_done_requests_closed_2021_datasd.csv')
get_it_done_2020 = pd.read_csv('get_it_done_requests_closed_2020_datasd.csv')
get_it_done_2019 = pd.read_csv('get_it_done_requests_closed_2019_datasd.csv')
get_it_done_2018 = pd.read_csv('get_it_done_requests_closed_2018_datasd.csv')
get_it_done_2017 = pd.read_csv('get_it_done_requests_closed_2017_datasd.csv')
get_it_done_2016 = pd.read_csv('get_it_done_requests_closed_2016_datasd.csv')

get_it_done_closed = pd.concat([get_it_done_2016, get_it_done_2017, get_it_done_2018, get_it_done_2019, 
                                get_it_done_2020, get_it_done_2021, get_it_done_2022])

# filter for "Street Light Maintenance" and export to csv
street_light_closed = get_it_done_closed.loc[get_it_done_closed['service_name'] == 'Street Light Maintenance']

#print(street_light_closed['service_name'].unique())
street_light_closed.to_csv('street_light_closed.csv', index=False)


# check how many entries are in the open and closed databases
#print(street_light_closed['status'].unique())
# 7949 open entries
street_light_open.info(verbose = True)
# 45603 closed entries
street_light_closed.info(verbose = True)


# first thing noticed was some of the closed reports were referred. Seperate referred and closed reports and export to csv
# 791 referred entries
street_light_referred = street_light_closed[street_light_closed['status'] == 'Referred']
street_light_referred.to_csv('street_light_referred.csv', index=False)
street_light_referred.info(verbose = True)

# 44812 closed entries not referred
street_light_closed_no_refer = street_light_closed[street_light_closed['status'] == 'Closed']
street_light_closed_no_refer.to_csv('street_light_closed_no_refer.csv', index=False)
street_light_closed_no_refer.info(verbose = True)