import time

def current_millis():
    return time.time_ns() // 1000000