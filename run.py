import time

from core.tracker import Tracker

if __name__ == '__main__':
    with Tracker() as tracker:

        run = 0
        print(f"{'Run':^6s} | {'Task':^20s} | {'Program':^20s} | {'Window name'}")
        while True:
            run += 1
            run %= 999_999
            data = tracker.parser_info
            print(f"\r{run:6d} | {data.task:20s} | {data.program:20s} | {data.window_name:100s}", end='')
            time.sleep(0.2)
