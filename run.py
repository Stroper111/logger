import time

from core import Session

if __name__ == '__main__':
    time_start = time.time()
    print("Program running in the background, don't worry ...")

    with Session() as session:
        while True:
            # Sleep and run.
            time.sleep(0.5)
            session.run()

            # Every x minutes auto save the summary
            time_passed = time.time() - time_start
            if time_passed > 60 * 5:
                session.save_summary()
                time_start = time.time()
