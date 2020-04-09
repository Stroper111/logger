import time

from core import Session

if __name__ == '__main__':
    time_start = time.time()
    print("Program running in the background, don't worry ...")

    with Session() as session:
        while True:
            # Sleep and run.
            time.sleep(0.2)
            session.run()
