import random, time, os, signal, hcsr04, operator


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
        self.distance = 999

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def sense_direction(self):
        # Getting readings from all the sensors in this direction
        self.distance = 999
        for sensor in self.sensors:
            d = sensor.sense()
            if d < self.distance:
                self.distance = d
                if d < sensor.threshold:
                    return True
        return False


class SensorArray():
    # This is a sensor array object
    # Direction and free direction objects are added to the sensor array object
    def __init__(self, drone, default_direction):
        self.directions = set()
        self.free_directions = set()
        self.geopoint_history = {}
        self.drone = drone
        self.default_direction = [default_direction]

    def add_direction(self, direction):
        self.directions.add(direction)

    def add_free_direction(self, free_direction):
        self.free_directions.add(free_direction)

    def start_session(self):
        print("Running drone sensor systems")
        while self.drone.travelling:
            self.sense_array()
            time.sleep(1)
        print("Stopping drone sensor systems")

    def sense_array(self):
        # Getting readings from all the sensors in all directions
        free = []
        for direction in self.directions:
            obstruction = direction.sense_direction()
            if not obstruction:
                free.append(direction)
        if len(free) != len(self.directions):
            self.respond(set(free))

    def action_type(self, directions, geopoint):
        if directions - self.geopoint_history[geopoint]:
            action_type = "Unknown"
        elif directions:
            action_type = "Known"
        elif self.free_directions - self.geopoint_history[geopoint]:
            action_type = "Free"
        else:
            action_type = "Default"

        return action_type

    def respond(self, directions):
        geopoint = self.drone.get_location()

        if geopoint not in self.geopoint_history:
            self.geopoint_history[geopoint] = set()

        action_type = self.action_type(directions, geopoint)

        moves = directions - self.geopoint_history[geopoint] or directions or \
                self.free_directions - self.geopoint_history[geopoint] or self.default_direction
        move = sorted(moves, key=operator.attrgetter("distance"))[-1]
        self.geopoint_history[geopoint].add(move)

        print("Obstruction Detected.... Moving in direction:", move.vector, "Action type: ", action_type)

        self.drone.response_move = move.vector
        os.kill(os.getpid(), signal.SIGUSR1)
