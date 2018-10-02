from sensor_array import *


move = None


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