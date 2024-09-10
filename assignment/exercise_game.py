"""
Response time - single-threaded

WLAN networking code obtained from https://projects.raspberrypi.org/en/projects/get-started-pico-w/2
"""

from machine import Pin, reset
import time
import random
import json
import network
import urequests as requests


N: int = 10 # number of flashes
sample_ms = 10.0
on_ms = 500 # user must hit button within this time (ms)
ssid = 'YOUR WIFI HERE'
password = 'YOUR PASSWORD HERE'


def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip


def random_time_interval(tmin: float, tmax: float) -> float:
    """return a random time interval between max and min"""
    return random.uniform(tmin, tmax)


def blinker(N: int, led: Pin) -> None:
    # let user know game started / is over

    for _ in range(N):
        led.high()
        time.sleep(0.1)
        led.low()
        time.sleep(0.1)


def write_json(json_filename: str, data: dict) -> None:
    """Writes data to a JSON file.

    Parameters
    ----------

    json_filename: str
        The name of the file to write to. This will overwrite any existing file.

    data: dict
        Dictionary data to write to the file.
    """

    with open(json_filename, "w") as f:
        json.dump(data, f)


def scorer(t: list[int | None]) -> None:
    # collate results
    misses = t.count(None)
    print(f"You missed the light {misses} / {len(t)} times")

    t_good = [x for x in t if x is not None]

    print(t_good)

    # add key, value to this dict to store the minimum, maximum, average response time
    # and score (non-misses / total flashes) i.e. the score a floating point number
    # is in range [0..1]
    data = {}

    # average
    data["average"] = sum(t_good)/len(t_good)
    # minimum
    data["minimum"] = min(t_good)
    # maximum
    data["maximum"] = max(t_good)

    # make dynamic filename and write JSON

    now: tuple[int] = time.localtime()

    now_str = "-".join(map(str, now[:3])) + "T" + "_".join(map(str, now[3:6]))
    filename = f"score-{now_str}.json"

    print("write", filename)

    write_json(filename, data)

    # upload data to firebase realtime database
    r = requests.put(f"https://(YOUR ID HERE).firebaseio.com/{filename}", data=json.dumps(data))
    print(r)
    if r.status_code == 200:
        print("Data uploaded successfully!")


if __name__ == "__main__":
    print("Successfully imported requests.")

    try:
        ip = connect()

        led = Pin("LED", Pin.OUT)
        button = Pin(14, Pin.IN, Pin.PULL_UP)

        t: list[int | None] = []

        blinker(3, led) # start of game

        for i in range(N):
            time.sleep(random_time_interval(0.5, 5.0))

            led.high()

            tic = time.ticks_ms()
            t0 = None
            while time.ticks_diff(time.ticks_ms(), tic) < on_ms:
                if button.value() == 0:
                    t0 = time.ticks_diff(time.ticks_ms(), tic)
                    led.low()
                    break
            t.append(t0)

            led.low()

        blinker(5, led) # end of game

        scorer(t)

    except KeyboardInterrupt:
        machine.reset()
