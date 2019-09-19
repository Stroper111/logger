
import datetime
import os
import csv
import yaml

from actions import Action


class InputOutput:
    def __init__(self):
        self.location = None
        self.filename = None
        
    def ceate(self, location, filename):
        if not os.path.exists(os.path.join(location, filename)):
            with open(self.filename, "w") as file:
                pass
                
    def read_yaml(self, location):
        with open(location, "rb") as stream:
            data = yaml.safe_load(stream)
        return data


class Console:
    io = InputOutput()
    
    def __init__(self):
        self.actions = [Action(**each) for each in self.io.read_yaml("console.yaml")]
        
    def _welcome(self):
        action = "\n".join(map(Action.show, self.actions))
        print("\n\nWelcome to this simple logger, you can use: \n", action,
              "Alternatively you can save a log by adding a comment or space after the end commands.\n\n")
              
    def _action(self, command):
        return


class Logger(Console):
    filename = "Serpentine.log"
    format = "%Y-%m-%d,%H:%M:%S"
    headers = ["Start day", "Start time", "End day", "End time", "Minutes", "comment"]

    def __init__(self):
        super().__init__()
        self.time_start = None
        self.time_end = None
        self.time_diff = None

    @staticmethod
    def get_time():
        return datetime.datetime.now()

    def get_time_diff(self):
        return max(round((self.time_end - self.time_start).seconds // 60 / 10) * 10, 15)

    def set_time(self, key):
        setattr(self, "time_" + key, self.get_time())
        print(f"Log {key}ed at:", getattr(self, "time_" + key).strftime(self.format))

    def start_recording(self, _):
        self.set_time( "start")

    def stop_recording(self, msg):
        self.set_time("end")

        if msg:
            self.save_recording(msg)

    def quit_recording(self, _):
        print("Exiting program")
        exit(0)

    def save_recording(self, msg):
        if not self.time_start:
            print("Didn't started a log yet, failed to save")
            return

        if not self.time_end:
            self.stop_recording()

        self.time_diff = self.get_time_diff()
        print("Worked for about: %s minutes on: %s" % (self.time_diff, msg))

        try:
            with open(self.filename, "a") as file:
                file.write(f"{self.time_start.strftime(self.format)},"
                           f"{self.time_end.strftime(self.format)},"
                           f"{self.time_diff},"
                           f"{msg}\n")
        except PermissionError:
            print("Unable to save due to permission error, please close the file.")

    def show_recording(self, _):
        with open(self.filename, "r") as file:
            print("\n", "".join(file.readlines()))

    def listen(self):
        command = None

        while command == None:
            command = input()

            for options in ["start", "stop", "save", "show", "quit"]:
                if [True for each in getattr(self, options) if command.split(" ")[0] == each]:
                    msg = " ".join(command.split(" ")[1:])
                    getattr(self, options + "_recording")(msg)
            command = None


if __name__ == "__main__":
    test = Logger()
    test.listen()
