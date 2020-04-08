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
    _format_time = '%Y %b %d, %a %H:%M:%S +0000'

    def __init__(self, task: str = 'idle', program: str = 'unknown', window_name: str = 'None'):
        self.task = task
        self.program = program
        self.window_name = window_name
        self.time_start: datetime = datetime.now()
        self.time_end: Union[datetime, None] = None

    def __str__(self):
        return f"Task: {self.task:20s}, Program: {self.program:20s}, window name: {self.window_name}" \
               f"\n\tStart time: {self.time_start.strftime(self._format_time)}" \
               f"\n\tEnd time  : {self.time_end.strftime(self._format_time) if self.time_end is not None else 'None'}" \
               f"\n\tDuration  : {self.time_end - self.time_start if self.time_end is not None else 'unknown'}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other: 'Job'):
        return self.task == other.task and self.program == other.program and self.window_name == other.window_name

    def __ne__(self, other):
        return self.task != other.task or self.program != other.program or self.window_name != other.window_name

    @property
    def timers(self):
        return dict(time_start=datetime.strftime(self.time_start, '%Y-%m-%dT%H:%M:%S'),
                    time_end=datetime.strftime(self.time_end, '%Y-%m-%dT%H:%M:%S'),
                    duration=self.time_end - self.time_start)

    @property
    def duration(self):
        if self.time_end is None:
            return datetime.now() - self.time_start
        return self.time_end - self.time_start

    @property
    def serialize(self):
        """ The JSON serialized dump of a Job.  """
        return json.dumps(self, indent=4, cls=JobEncoder)

    @staticmethod
    def deserialize(object) -> 'Job':
        """ Decode a serialized dump of a Job.  """
        return json.loads(object, cls=JobDecoder)

    def stop(self):
        self.time_end = datetime.now()


if __name__ == '__main__':
    test = Job()
    test.stop()

    serialized = test.serialize
    deserialized = test.deserialize(serialized)

    print(serialized)
    print(deserialized)
