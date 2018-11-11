#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Python weekend Kiwi.com - Entry task
https://gist.github.com/martin-kokos/6ccdeeff45a33bce4849567b0395526c

Usage:  python find_combinations.py < flights.csv > output.txt
        cat flights.csv | find_combinations.py

"""

__author__ = "Jan Kammermayer"
__email__ = "honza.kammermayer@gmail.com"

import sys
from datetime import datetime, timedelta
import csv

class Flight(object):
    """ Class flight """

    def __init__(self, source, destination, departure, arrival, flight_number, price, bags_allowed, bag_price):
        self.source = source
        self.destination = destination
        self.departure = datetime.strptime(departure, '%Y-%m-%dT%H:%M:%S')
        self.arrival = datetime.strptime(arrival, '%Y-%m-%dT%H:%M:%S')
        self.flight_number = flight_number
        self.price = int(price)
        self.bags_allowed = int(bags_allowed)
        self.bag_price = int(bag_price)

    def find_all_possibilities(self, all_flights, bags):
        """ Find all possibilities of flight """

        return [flight for flight in all_flights if self.check_flight(flight, bags)]

    def check_flight(self, next_flight, bags):
        """ Check if flight is from source, transfer time and bags """

        return self.destination == next_flight.source and \
                (next_flight.departure - self.arrival > timedelta(hours=1)) and \
                (next_flight.departure - self.arrival < timedelta(hours=4)) and \
                (next_flight.bags_allowed >= bags)

    def __str__(self):
        return self.flight_number

def itinerary(flight, bags, all_flights, path = []):
    """ Find all possible paths for flight """

    path.append(flight)
    possibilities = flight.find_all_possibilities(all_flights, bags)

    if validate_path(path):
        print_path(path, bags)

    if possibilities:
        for next_flight in possibilities:
            itinerary(next_flight, bags, all_flights, path)
            path.pop(len(path) - 1)

def load_data(csv_file):
    """ Load data from file and create objects Flight """

    next(csv_file)  # Skip header
    return [Flight(*flight) for flight in csv.reader(csv_file)]

def validate_path(path):
    """ Check if path is valid """

    if len(path) < 2:
        return False

    for x, a in enumerate(path):
        for b in path[x + 1:]:
            if a.source == b.source and a.destination == b.destination:
                return False

    return True

def print_path(path, bags):
    """ Print path """

    price = 0
    print('{} -> '.format(path[0].source), end='')
    for flight in path:
        print('{} ({})-> '.format(flight.destination, flight.flight_number), end='')
        price += flight.price + bags * flight.bag_price
    print("{}".format(price))

if __name__ == '__main__':
    file = open('flights.csv')
else:
    file = sys.stdin
all_flights = load_data(file)

for bags in range(0, 3):
    print('### {} bags ###'.format(bags))
    flights_by_bags = [flight for flight in all_flights if flight.bags_allowed >= bags]
    for flight in flights_by_bags:
        itinerary(flight, bags, all_flights, [])
