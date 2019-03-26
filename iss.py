#!/usr/bin/env python
import requests
import ast
import turtle
import time

__author__ = "Michael McKenzie"


def api_request(url):
    """Obtains text data from url and removes unicode"""
    request = requests.get(url)
    return ast.literal_eval(request.text)


def iss_info():
    """Obtains list of astronauts currently in space, name of spacecraft, and total number of astronauts in space"""
    r = api_request('http://api.open-notify.org/astros.json')
    astro_names = [item['name'] for item in r['people']]
    print("\nSPACECRAFT AND CREW DETAILS \nThe total number of astronauts in space: {} \nName of spacecraft: {} \nNames of astronauts on this spacecraft: {}\n\n".format(
        r['number'], r['people'][0]['craft'], astro_names))


def iss_locator():
    """Obtains the current geographic coordinates (lat/long) of ISS alog with a timestamp"""
    global lat, long
    r = api_request('http://api.open-notify.org/iss-now.json')
    lat = r['iss_position']['latitude']
    long = r['iss_position']['longitude']
    print("CURRENT POSITION \nLatitude: {} \nLongitude: {}\nTimestamp: {}\n".format(
        r['iss_position']['latitude'], r['iss_position']['longitude'], r['timestamp']))


def iss_position():
    """Uses turtle module to visualize ISS position above Earth"""
    screen = turtle.Screen()
    screen.setup(720, 360)
    screen.setworldcoordinates(-180, -90, 180, 90)
    screen.addshape("iss.gif")
    turtle.shape("iss.gif")
    screen.bgpic("map.gif")
    turtle.screensize(720, 360)
    turtle.penup()
    turtle.goto(float(lat), float(long))
    indy_img = turtle.Turtle()
    indy_img.dot()
    indy_img.color("yellow")
    indy_img.penup()
    indy_img.goto(float(indy['lon']), float(indy['lat']))
    turtle.done()


def indy_iss_pass():
    global indy
    indy = {'lat': 39.7684, 'lon': -86.1581}
    r = requests.get("http://api.open-notify.org/iss-pass.json", params=indy)
    r = ast.literal_eval(r.text)
    pass_time = time.ctime(r['response'][0]['risetime'])
    print "NEXT ISS PASS OVER INDIANAPOLIS, IN\n", pass_time


if __name__ == '__main__':
    iss_info()
    iss_locator()
    indy_iss_pass()
    iss_position()
