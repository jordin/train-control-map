"""
Programmer: Jordin McEachern & Serge Toutsenko
Program: train machine map
Created on: 2019-12-06
File: stations.py
Description: stores the positions of all the stations
"""
# available station range
station_ids = range(24)

# numerical offset to force all stations to be two-digits
# this simplifies the parsing for the train machine
station_offset = 10

# station coordinates and direction
stations = [
    (217, 496, 'w'),
    (395, 496, 'w'),
    (505, 496, 'w'),
    (654, 496, 'w'),
    (764, 496, 'w'),
    (942, 496, 'w'),
    (1149, 336, 's'),
    (1149, 229, 's'),
    (942, 69, 'e'),
    (764, 69, 'e'),
    (654, 69, 'e'),
    (505, 69, 'e'),
    (395, 69, 'e'),
    (217, 69, 'e'),
    (10, 229, 'n'),
    (10, 336, 'n'),
    (361, 528, 'w'),
    (798, 528, 'w'),
    (798, 37, 'e'),
    (361, 37, 'e'),
    (627, 448, 'w'),
    (804, 448, 'w'),
    (532, 117, 'e'),
    (355, 117, 'e')
]
