import functools
import inspect
import yaml
import sys
import time

from . import trackers as pyfunctrackers

def _track_callabe(param, *trackers, msg_fmt=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = int(time.time())
            ret = func(*args, **kwargs)
            end_time = int(time.time())

            tracker_kwargs = dict(
                parameter=param,
                function=func, return_value=ret,
                args=args, kwargs=kwargs,
                start_time=start_time, end_time=end_time,
            )
            tracker_kwargs["message"] = msg_fmt.format(**tracker_kwargs) if msg_fmt else None

            for _tracker in trackers:
                _tracker.do(**tracker_kwargs)

            return ret
        return wrapper
    return decorator

def configure(callable_configuration, trackers=[], is_indirect_call=False):

    _caller = inspect.getmodule(
        inspect.stack()[1+(1 if is_indirect_call else 0)][0]
    )
    if _caller is None:
        _caller = sys.modules['__main__']

    for fn, fn_conf in callable_configuration.items():

        ref = fn.__name__ if callable(fn) else fn

        if isinstance(fn_conf, dict):
            param = fn_conf.get("parameter", ref)
            msg = fn_conf.get("message", None)
        else:
            param, msg = ref, None

        _ptr = _caller
        if len(_ref_names := ref.split(".")) > 1:
            ref = _ref_names.pop(-1)
            for _ref_node in _ref_names:
                _ptr = _ptr.__dict__[_ref_node]

        fn = getattr(_ptr, ref)
        setattr(_ptr, ref, _track_callabe(param, *trackers, msg_fmt=msg)(fn))

def enable(conf_path, trackers=[]):
    with open(conf_path, 'r') as fd:
        conf = yaml.safe_load(fd)

    if "trackers" in conf:
        if "logger" in conf["trackers"]:
            logger_kwargs=dict(
                log_file=conf["trackers"]["logger"].get("log_file", ".tracker_log")
            )
            trackers.append(pyfunctrackers.logger.Logger(**logger_kwargs))

    configure(conf["functions"], trackers=trackers, is_indirect_call=True)