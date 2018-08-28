#!/usr/bin/env python2

import sys
import requests
import argparse
import turtle
import time


def find_astronauts():
    '''Sends an api request to find out the current astronauts on the ISS'''
    r = requests.get("http://api.open-notify.org/astros.json")
    return r.json()


def indy_time():
    '''Sends an api request to get the next time
     the ISS will pass over Indianapolis'''
    coords = {'lat': 39.7684, 'lon': -86.1581}
    r = requests.get("http://api.open-notify.org/iss-pass.json", params=coords)
    t = time.ctime(r.json()['response'][0]['risetime'])
    return t


def find_iss():
    '''Creates a plot of the world map with the position of
    the ISS and when the ISS will pass over Indianapolis'''
    r = requests.get("http://api.open-notify.org/iss-now.json",)
    iss_info = r.json()
    iss_position = iss_info['iss_position']
    iss_longitude = iss_position['longitude']
    iss_latitude = iss_position['latitude']

    screen = turtle.Screen()
    screen.setup(720, 360)
    screen.setworldcoordinates(-180, -90, 180, 90)
    screen.bgpic("map.gif")
    screen.register_shape("iss.gif")

    t = turtle.Turtle()
    t.shape("iss.gif")
    t.setheading(90)
    t.penup()
    t.goto(float(iss_longitude), float(iss_latitude))

    location = turtle.Turtle()
    location.penup()
    location.color('yellow')
    location.goto(-86.1581, 39.7684)
    location.shape('circle')
    location.resizemode('user')
    location.shapesize(0.2)
    location.write(indy_time())

    screen.exitonclick()


def create_parser():
    """Creates an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--astros',
                        help='finds astronauts', action='store_true')
    parser.add_argument('-i', '--iss',
                        help='finds iss', action='store_true')
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
Number of astronauts in space:""", found_astronauts["number"]
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
