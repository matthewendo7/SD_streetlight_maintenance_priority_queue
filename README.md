# SD_streetlight_maintenance_priority_queue

uses the closed San Diego Get It Done Reports data from 2016-2022 and open San Diego Get It Done Reports data (accessed 9/22/2022) from https://data.sandiego.gov/datasets/get-it-done-311/. 

sd_streetlight_filter.py: filters away non-streetlight requests

sd_streetlight_zipcodes.py: adds zip code data to reports missing zip codes

sd_streetlight_population_income.py: adds population density (in lieu of foot traffic data) and median household income (in lieu of crime rate data) to all reports

sd_streetlight_priority_queue.py: calculates priority score, builds priority queue, minor calculations to compare priority queue with actual closed reports
