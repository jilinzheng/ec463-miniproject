"""
Don't Blink!
The premier Pi Pico WH response time game!

WLAN networking code obtained from https://projects.raspberrypi.org/en/projects/get-started-pico-w/2
"""

from machine import Pin, reset
import time
import random
import json
import network
import urequests as requests


# response time game configuration
N: int = 10 # number of flashes
sample_ms = 10.0
on_ms = 500 # user must hit button within this time (ms)

# Pico GPIO + LED configuration
led = Pin("LED", Pin.OUT)
button = Pin(14, Pin.IN, Pin.PULL_UP)
play_button = Pin(2, Pin.IN, Pin.PULL_UP) # to play the game multiple times without restarting script

# wifi, cloud storage (firebase) configuration
ssid = '{YOUR WIFI NAME}'
password = '{YOUR WIFI PASSWORD}'
firebase = 'https://{YOUR DATABASE NAME}.firebaseio.com/'
user_email = '{YOUR EMAIL, WITHOUT @ AND SUBSEQUENT LETTERS}' # DO NOT INLCUDE '@' AND SUBSEQUENT LETTERS; used for firebase


def connect():
    """ connect to WLAN """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    i = 0 # simple timeout logic
    while wlan.isconnected() == False and i != 10:
        print('Waiting for connection...')
        time.sleep(1)
        i+=1
    if i == 10: # if connection unsuccessful
        machine.reset()
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip


def random_time_interval(tmin: float, tmax: float) -> float:
    """ return a random time interval between max and min """
    return random.uniform(tmin, tmax)


def blinker(N: int, led: Pin) -> None:
    """ let user know game started / is over """
    for _ in range(N):
        led.high()
        time.sleep(0.1)
        led.low()
        time.sleep(0.1)


def write_json(json_filename: str, data: dict) -> None:
    """ write data to a JSON file """
    with open(json_filename, "w") as f:
        json.dump(data, f)


def scorer(t: list[int | None]) -> None:
    """ score user performance """

    # collate results
    misses = t.count(None)
    print(f"You missed the light {misses} / {len(t)} times")

    t_good = [x for x in t if x is not None]

    print(t_good)

    # add key, value to this dict to store the minimum, maximum, average response time
    # and score (non-misses / total flashes) i.e. the score a floating point number
    # is in range [0..1]
    data = {}
    data["average"] = sum(t_good)/len(t_good)
    data["minimum"] = min(t_good)
    data["maximum"] = max(t_good)

    # make dynamic filename
    now: tuple[int] = time.localtime()
    now_str = "-".join(map(str, now[:3])) + "T" + "_".join(map(str, now[3:6]))
    filename = f"score-{now_str}.json"

    # write JSON locally
    #print("write", filename)
    #write_json(filename, data)

    # upload JSON data to firebase realtime database, under the appropriate user
    r = requests.put(firebase+user_email+'/'+filename, data=json.dumps(data))
    if r.status_code == 200:
        print("Data uploaded successfully!")
    else:
        print("Unsuccessful upload...try again...")


def play():
    try:
        connect() # connect to wifi

        # set up score list
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

        # score user + upload data
        scorer(t)

    except KeyboardInterrupt:
        machine.reset()


if __name__ == "__main__":
    print("Welcome to 'Don't Blink', the premier Pi Pico WH response time game!")
    print("Hit the button connected to GP2 and GND to start!")
    while True:
        if play_button.value() == 0:
            print("Game rule: simply hit the button connected to GP14 and GND when the LED flashes! Compete to be the fastest!")
            play()
            print("Want to play again? Hit the GP2/GND button again! Or you can hit CTRL+C to quit...but why would you ever do that?")
