import random
import time
import os


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
