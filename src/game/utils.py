import time

def current_millis():
    return time.time() * 1000

def format_millis(millis: float) -> str:
    if millis < 0:
        return str(int(-millis // 1000) + 1)

    millis = round(millis / 1000, 2)
    mins = int(millis // 60)
    millis -= mins * 60

    rep = f"{mins}:" + f"{millis:.2f}".zfill(5)
    return str(rep)