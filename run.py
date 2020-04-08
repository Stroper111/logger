import time

from core import Session

if __name__ == '__main__':
    time_start = time.time()

    with Session() as session:
        while True:
            # Sleep and run.
            time.sleep(0.2)
            session.run()

            # Print after some time
            if time.time() - time_start > 10:
                time_start = time.time()
                session.print()
