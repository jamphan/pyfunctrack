import functools
import inspect
import yaml
import time

def _track_callabe(param, *trackers):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = int(time.time())
            ret = func(*args, **kwargs)
            end_time = int(time.time())

            tracker_kwargs = dict(
                parameter=param,
                function=func.__name__, return_value=ret,
                args=args if len(args) > 0 else None,
                kwargs=kwargs if len(kwargs) > 0 else None,
                start_time=start_time, end_time=end_time
            )

            for _tracker in trackers:
                _tracker(**tracker_kwargs)

            return ret
        return wrapper
    return decorator

def configure(callable_configuration, trackers=[], is_indirect_caller=False):

    _caller = inspect.getmodule(
        inspect.stack()[1+(1 if is_indirect_caller else 0)][0]
    )

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
        setattr(_ptr, ref, _track_callabe(param, *trackers)(fn))

def enable(conf_path, trackers=[]):
    with open(conf_path, 'r') as fd:
        configuration = yaml.safe_load(fd)

    if "trackers" in configuration:
        if "printer" in configuration["trackers"]:
            trackers.append(printer)
        if "remote" in configuration["trackers"]:
            trackers.append(remote_factory(**configuration["trackers"]["remote"]))

    configure(configuration["functions"], trackers=trackers, is_indirect_caller=True)