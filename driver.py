from sensor_array import *
import threading, time


class Drone:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.current = start
        self.travelling = True
        self.lock = threading.Lock()

    def get_location(self):
        return tuple(self.current)

    def respond(self, move):
        self.lock.acquire()
        for index, axis in enumerate(move):
            self.current[index] += 0.00001 * axis
        print(self.current)
        self.lock.release()

    def move(self):
        while self.current != self.end:
            self.lock.acquire()
            for index, attr in enumerate(zip(self.current, self.end)):
                if attr[0] < attr[1]:
                    self.current[index] = round(self.current[index] + 0.00001, 5)
                if attr[0] > attr[1]:
                    self.current[index] = round(self.current[index] - 0.00001, 5)
            print(self.current)
            self.lock.release()
            time.sleep(1)
        self.travelling = False
        print("Reached destination")


def main():
    start = [12.29053, 76.64510, 10.00000]
    end = [12.29060, 76.64520, 10.00000]

    drone = Drone(start, end)
    sa = SensorArray(drone)

    directions = [
        Direction([1, 0, 0], 0),
        Direction([0, 0, 1], 1),
        Direction([-1, 0, 0], 2),
        Direction([0, 0, -1], 3),
        Direction([0, 1, 0], 4),
        Direction([0, -1, 0], 5),
    ]

    # Note that directions 5 and 6 have no sensors assigned to them

    for j in range(4):
        for i in range(4):
            directions[j].add_sensor(Sensor((4 * j) + i, (4 * j) + i + 4))

    for direction in directions:
        sa.add_direction(direction)

    t = threading.Thread(target=sa.start_session)
    t.start()

    drone.move()


main()