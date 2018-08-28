#!/usr/bin/env python2

import re
import sys
import urllib
import requests
import argparse
import turtle

def find_astronauts():
    r = requests.get("http://api.open-notify.org/astros.json")
    return r.json()


def find_iss():
    r = requests.get("http://api.open-notify.org/iss-now.json")
    iss_info = r.json()
    # iss_timestamp = iss_info['timestamp']
    iss_position = iss_info['iss_position']
    iss_longitude = iss_position['longitude']
    iss_latitude = iss_position['latitude']

    # print iss_timestamp, iss_longitude, iss_latitude

    screen = turtle.Screen()
    screen.setup(720,360)
    screen.setworldcoordinates(-180, -90, 180, 90)
    screen.bgpic("map.gif")

    screen.register_shape("iss.gif")
    t = turtle.Turtle()
    t.shape("iss.gif")
    t.setheading(90)

    t.penup()
    t.goto(iss_longitude, iss_latitude)

    # location = turtle.Turtle()
    # location.penup()
    # location.color('yellow')
    # location.goto(22,55)
    # location.dot(5)
    # location.hideturtle()
    # turtle.done()


def create_parser():
    """Creates an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-a','--astros',
                        help='finds astronauts')
    parser.add_argument('-i','--iss',
                        help='finds iss')
    return parser


def main(args):
    """Parse args, scrape webpage, scan with regex"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)
    

    # Finds all astronuts and gives their craft and the number of astronauts
    if parsed_args.astros:
        found_astronauts = find_astronauts()
        print """
Number of astronauts in space:""",found_astronauts["number"]
        print """
Astronaut names and craft: 
"""
        for astronaut in found_astronauts["people"]:
            print astronaut["name"], astronaut["craft"]

    # Finds coordinates of the ISS
    if parsed_args.iss:
        find_iss()

if __name__ == '__main__':
    main(sys.argv[1:])
