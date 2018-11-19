import threading, time, signal
from sensor_array import *
# import import RPi.GPIO as GPIO


# GPIO.setmode(GPIO.BCM)


def set_trigger_pins(pins):
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)


def set_echo_pins(pins):
    for pin in pins:
        GPIO.setup(pin, GPIO.IN)


drone = None


def handle_signal(signum, frame):
    global drone
    for index, axis in enumerate(drone.response_move):
       drone.current[index] = round(drone.current[index] + 0.00001 * axis, 5)
    # This line causes a bug related to renterant tasks...
    # This line of code is for experimentation purposes only and will not be included in the final build 
    print("Current position:", drone.current)


signal.signal(signal.SIGUSR1, handle_signal)


class Drone:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.current = start
        self.travelling = True
        self.response_move = None

    def get_location(self):
        return tuple(self.current)

    def move(self):
        while self.current != self.end:
            for index, attr in enumerate(zip(self.current, self.end)):
                if attr[0] < attr[1]:
                    self.current[index] = round(self.current[index] + 0.00001, 5)
                if attr[0] > attr[1]:
                    self.current[index] = round(self.current[index] - 0.00001, 5)
            print("Current position:", self.current)
            time.sleep(1)
        self.travelling = False
        print("Reached destination")


def main():
    global drone
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

    time.sleep(0.2)
    drone.move()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as ke:
        print("Goodbye....")
    finally:
        # GPIO.cleanup()
        pass
