import time


class Scheduler:

    def __init__(self):
        self.interval = 300

    def start(self):

        print("Scheduler Started")

        while True:

            print("Running Scan Cycle...")

            # Scanner akan dipanggil di sini

            print("Waiting 5 minutes...\n")

            time.sleep(self.interval)