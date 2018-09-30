import random
import time
import os


move = None


class Sensor():
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
    def __init__(self, vector, id):
        self.vector = vector
        self.id = id
        self.sensors = []
        self.distance = 400

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def sense_direction(self):
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
    def __init__(self, vector, id):
        self.vector = vector
        self.id = id

    def __str__(self):
        return "Free direction: " + str(self.vector)

class SensorArray():
    def __init__(self):
        self.directions = []
        self.free_directions = []

    def add_direction(self, direction):
        self.directions.append(direction)

    def add_free_direction(self, free_direction):
        self.free_directions.append(free_direction)

    def sense_array(self):
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
        # Code to respond to the obstruction
        # Obstructed may be used in te future

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


def main():
    sa = SensorArray()

    directions = [
        Direction([1, 0, 0], 0),
        Direction([0, 0, 1], 1),
        Direction([-1, 0, 0], 2),
        Direction([0, 0, -1], 3),
    ]
    free_directions = [
        FreeDirection([0, 1, 0], 4),
        FreeDirection([0, -1, 0], 5),
    ]

    for j in range(4):
        for i in range(4):
            directions[j].add_sensor(Sensor((4 * j) + i, (4 * j) + i + 4))

    for direction in directions:
        sa.add_direction(direction)

    for free_direction in free_directions:
        sa.add_free_direction(free_direction)

    print(sa)

    while(1):
        sa.sense_array()
        print("-" * 159)
        time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Good Bye....")