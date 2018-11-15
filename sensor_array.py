import random
import time
import os
from math import radians, cos, sin, asin, sqrt


# move = None

class Sensor():
    # This is a sensor object
    # It takes echo and treshold pin numbers as arguments during init
    # Treshold is an optional argument to tune the sensitivity of the sensor
    def __init__(self, echo, trigger, threshold=30):
        self.echo = echo
        self.trigger = trigger
        self.threshold = threshold

    def sense(self):
        # Code to read data from the sensor
        return random.randrange(0, 400)

    def __str__(self):
        return "Sensor - Echo: " + str(self.echo) + " Trigger: " + str(self.trigger)


class Direction():
    # This is a direction object
    # Multiple sensors can be facing the same direction
    # It takes a direction vector and a direction id dufing init
    # Direction vector is given in [i, j, k] format, id is a unique identifier for the direction
    # Sensor objects are added to the direction object
    def __init__(self, vector, id):
        self.vector = vector
        self.id = id
        self.sensors = []
        self.distance = 400

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def sense_direction(self):
        # Getting readings from all the sensors in this direction
        for sensor in self.sensors:
            self.distance = sensor.sense()
            if self.distance < sensor.threshold:
                return True
        return False

    def __str__(self):
        st = "Direction: " + str(self.vector) + "\n\t"
        st += "\n\t".join([str(sensor) for sensor in self.sensors])

        return st

class FreeDirection():
    # This is a free direction object
    # A free direction does not have any sensors facing that way
    # Free directions will be a last resort choice for the collision avoidance prediction
    # It takes a direction vector and a direction id dufing init
    # Direction vector is given in [i, j, k] format, id is a unique identifier for the direction
    def __init__(self, vector, id):
        self.vector = vector
        self.id = id

    def __str__(self):
        return "Free direction: " + str(self.vector)

class SensorArray():
    # This is a sensor array object
    # Direction and free direction objects are added to the sensor array object
    def __init__(self):
        self.directions = []
        self.free_directions = []

    def add_direction(self, direction):
        self.directions.append(direction)

    def add_free_direction(self, free_direction):
        self.free_directions.append(free_direction)

    def sense_array(self):
        # Getting readings from all the sensors in all directions
        free, obstructed = [], []
        for direction in self.directions:
            distance = direction.sense_direction()
            if distance:
                obstructed.append(direction)
            else:
                free.append(direction)
        if obstructed:
            self.respond(obstructed, free)
        else:
            # os.system("cls")
            print("Free to move in any direction")

    def respond(self, obstructed, free):
        # Code to respond to the obstruction (by picking a collision free direction)
        # Obstructed list may be used in te future

        global move
        if free:
            move = random.sample(free, 1)[0]
        elif self.free_directions:
            move = random.sample(self.free_directions, 1)[0]
        else:
            move = obstructed[0]
        self.pretty_print(obstructed, move)

        # Send an interrupt signal to main thread


    def delete_history():
        #reset history on reaching a new waypoint
        global history
        #code to upload history of previous way point to cloud
        #reset history
        history = {}

    def point_exists(lon2, lat2, alt2):
        global history
        #threshold is resolution of haversine
        #lon and lat in format of dd.mmmmmm or dd.mmmmss for east and north and negative dd.mmmmmm or dd.mmmmss  values for west and south
        threshold = 10
        for geopoint in history:
            lon1, lat1, alt1 = geopoint[0], geopoint[1], geopoint[2]
            lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
            #altitude based Calculation
            if (lat1, lon1) == (lat2, lon2) and abs(alt1 - alt2) < threshold:
                return geopoint

            # haversine formula
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a))
            r = 6372.8 # Radius of earth in kilometers. Use 3956 for miles
            distance = c * r * 1000
            if distance < threshold:
                return geopoint
        return False


    def respond_history(self, obstructed, free, lon, lat, alt):
        global history
        geopoint = point_exists(lon, lat, alt)
        if geopoint:
            moves = free - history[geopoint] or free
            move = random.sample(moves, 1)[0]
            history[geopoint].add(move)
        else:
            move = random.sample(free,1)[0]
            history[(lon, lat, alt)] = set(move)

        self.pretty_print(obstructed, move)




    def pretty_print(self, obstructed, move):
        # os.system("cls")
        for direction in obstructed:
            print("Object detected. Direction:", direction.vector, ", ID:", direction.id,
                ", Distance:", direction.distance)

        print("Move in direction:", move.vector, "- ID:", move.id)

    def __str__(self):
        st = ""
        for direction in self.directions:
            st += str(direction) + "\n"
        for free_direction in self.free_directions:
            st += str(free_direction) + "\n"
        return st
