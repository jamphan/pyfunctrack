import click
import runpy
import importlib
import inspect
import yaml
import sys
import types

import pyfunctrack

@click.command()
@click.option("--config", default="tracking.yaml")
@click.argument('target', nargs=1)
def cli(config, target):

    target = target.strip(".py")
    module = importlib.import_module(target)
    for symbol, ref in module.__dict__.items():
        globals()[symbol] = ref

    pyfunctrack.enable(config)

    with open(config, "r") as fd:
        conf = yaml.safe_load(fd)

    # Redefine symbols not tracked to capture new references
    # TODO: Need to capture Class Types
    for symbol, ref in module.__dict__.items():
        if symbol not in conf["functions"] and type(ref) != types.ModuleType and type(ref) == types.FunctionType:
            exec(inspect.getsource(ref), globals())

    main()

if __name__ == '__main__':
    cli()