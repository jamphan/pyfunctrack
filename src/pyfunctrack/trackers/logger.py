from .Tracker import Tracker

class Logger(Tracker):

    def __init__(self, log_file=".tracker_log"):
        self._log_file = log_file
        open(self._log_file, "w").close()

    def write(self, value):
        with open(self._log_file, 'a+') as fd:
            fd.write(value + '\n')

    def tracker_method(self, parameter=None, start_time=None, end_time=None, return_value=None, function=None, **kw):
        if isinstance(return_value, str):
            return_value = return_value.replace("\n", "\\n")
        self.write(f"{parameter.upper()}:{function} returned {return_value} and took {end_time-start_time} secs")