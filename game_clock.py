import time

start_time = 0.0


def start_the_clock():
    global start_time
    start_time = time.time()


def current_time():
    global start_time
    return time.time() - start_time


def elapsed_time(marker_time):
    return current_time() - marker_time


def game_time():
    # TODO Make pause-able
    pass

