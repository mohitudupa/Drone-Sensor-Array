import random, time, os, signal, hcsr04


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
        # return hcsr04.distance(trigger, echo)
        return random.randrange(0, 400)


class Direction():
    # This is a direction object
    # Multiple sensors can be facing the same direction
    # It takes a direction vector and a direction id dufing init
    # Direction vector is given in [i, j, k] format, id is a unique identifier for the direction
    # Sensor objects are added to the direction object
    def __init__(self, vector, id):
        self.vector = tuple(vector)
        self.id = id
        self.sensors = []

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def sense_direction(self):
        # Getting readings from all the sensors in this direction
        for sensor in self.sensors:
            if sensor.sense() < sensor.threshold:
                return True
        return False


class SensorArray():
    # This is a sensor array object
    # Direction and free direction objects are added to the sensor array object
    def __init__(self, drone):
        self.directions = []
        self.free_directions = []
        self.geopoint_history = {}
        self.drone = drone

    def add_direction(self, direction):
        self.directions.append(direction)

    def get_direction(self, directions):
        geopoint = self.drone.get_location()

        if geopoint in self.geopoint_history:
            moves = directions - self.geopoint_history[geopoint] or directions
            move = random.sample(moves, 1)[0]
            self.geopoint_history[geopoint].add(move)
        else:
            move = random.sample(directions, 1)[0]
            self.geopoint_history[geopoint] = {move, }
        print("Obstruction Detected.... Moving in direction:", move)

        return move

    def start_session(self):
        print("Running drone sensor systems")
        while self.drone.travelling:
            self.sense_array()
            time.sleep(1)
        print("Stopping drone sensor systems")

    def sense_array(self):
        # Getting readings from all the sensors in all directions
        free, obstructed = [], []
        for direction in self.directions:
            obstruction = direction.sense_direction()
            if obstruction:
                obstructed.append(direction.vector)
            else:
                free.append(direction.vector)
        if obstructed:
            self.respond(obstructed, free)

    def respond(self, obstructed, free):
        # Code to respond to the obstruction (by picking a collision free direction)
        # Obstructed list may be used in te future
        global move
        if free:
            move = self.get_direction(set(free))
        elif self.free_directions:
            move = self.get_direction(set(self.free_directions))
        else:
            move = obstructed[0].vecctor

        self.drone.response_move = move
        os.kill(os.getpid(), signal.SIGUSR1)
