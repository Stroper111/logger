from datetime import datetime
import json
from typing import Union


class JobEncoder(json.JSONEncoder):
    def default(self, object):
        if isinstance(object, datetime):
            return {'__datetime__': object.replace(microsecond=0).isoformat(sep=' ')}
        return {'__{}__'.format(object.__class__.__name__): object.__dict__}


class JobDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, object):
        class_name = f"__Job__"

        if class_name in object:
            job = Job()
            job.__dict__.update(object[class_name])
            return job

        if f"__datetime__" in object:
            return datetime.strptime(object['__datetime__'], '%Y-%m-%d %H:%M:%S')

        return object

class Job:
    _format_time = '%Y %b %d, %a %H:%M:%S'

    def __init__(self, task: str = 'Idle', program: str = 'unknown', window_name: str = 'None'):
        self.task = task
        self.program = program

        self._window_name = window_name
        self._window_name_alternatives = [self.window_name]

        self._time_start: datetime = datetime.now()
        self._time_end: Union[datetime, None] = None

    def __str__(self):
        window_names = '\n\tWindow name - '.join(self.window_names)
        return f"Task: {self.task:20s}\tProgram: {self.program:20s}\tDuration  : {self.duration}" \
               f"\n\tWindow name - {window_names}" \
               f"\n\tStart time  - {self._time_start.strftime(self._format_time)}" \
               f"\n\tEnd time    - {self._time_end.strftime(self._format_time) if self._time_end is not None else '-'}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other: 'Job'):
        return self.task == other.task and self.program == other.program

    def __ne__(self, other):
        return self.task != other.task or self.program != other.program

    @property
    def start_timer(self):
        return self._time_start.replace(microsecond=0).isoformat(sep=' ')

    @property
    def end_timer(self):
        return self._time_end.replace(microsecond=0).isoformat(sep=' ') if self._time_end is not None else 'None'

    @property
    def duration(self):
        if self._time_end is None:
            return datetime.now() - self._time_start
        return self._time_end - self._time_start

    @property
    def timers(self):
        return dict(time_start=self.start_timer,
                    time_end=self.end_timer,
                    duration=self.duration)
    @property
    def window_name(self):
        """ Cleans up the window name.  """
        return self._window_name.replace('\\', '/')

    @property
    def window_names(self):
        return [window_name.replace('\\', '/') for window_name in self._window_name_alternatives]

    @property
    def serialize(self):
        window_names = '\n\tAlternative - '.join(self.window_names)
        return f"\nTask: {self.task:20s}\tProgram: {self.program:20s}\tDuration  : {self.duration}" \
               f"\n\tWindow name - {window_names}" \
               f"\n\tStart time  - {self.start_timer}" \
               f"\n\tEnd time    - {self.end_timer}"

    @property
    def json_serialize(self):
        """ The JSON serialized dump of a Job.  """
        return json.dumps(self, indent=4, cls=JobEncoder)

    @staticmethod
    def json_deserialize(object) -> 'Job':
        """ Decode a serialized dump of a Job.  """
        return json.loads(object, cls=JobDecoder)

    def stop(self):
        self._time_end = datetime.now()

    def add_sub_window(self, window_name):
        self._window_name_alternatives.append(window_name)
        self._window_name_alternatives.sort()


if __name__ == '__main__':
    test = Job()
    test.stop()

    serialized = test.json_serialize
    deserialized = test.json_deserialize(serialized)

    print(serialized)
    print(deserialized)
