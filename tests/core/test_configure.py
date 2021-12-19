import pytest
from types import SimpleNamespace
import unittest.mock as mock

from src.pyfunctrack import configure

@pytest.fixture
def symbol_table():
    def foo(): return "foo"
    def bar(): return "bar"

    class Dog:
        def bark(self):
            return "woof!"

    return dict(
        foo=foo,
        bar=bar,
        red_dog=Dog()
    )

def get_module(symbol_table, mock=None):
    mod = SimpleNamespace(**symbol_table)
    if mock:
        mock.return_value = mod
    return mod

@mock.patch("src.pyfunctrack.core.inspect.getmodule")
def test_no_wrapping(mock_getmodule, symbol_table):

    # Given:
    module = get_module(symbol_table, mock=mock_getmodule)

    orig_foo_id = id(module.foo)
    orig_bar_id = id(module.bar)
    orig_redDog_id = id(module.red_dog)

    def check_callable(ptr, orig_id, name=None):
        if name:
            assert ptr.__name__ == name
            assert symbol_table[name] is ptr
        assert id(ptr) == orig_id
        assert not(hasattr(ptr, "__wrapped__"))

    # When:
    configure({})

    # # Then:
    check_callable(module.foo, orig_foo_id, name="foo")
    check_callable(module.bar, orig_bar_id, name="bar")
    check_callable(module.red_dog, orig_redDog_id)

@mock.patch("src.pyfunctrack.core.inspect.getmodule")
def test_function_wrapping(mock_getmodule, symbol_table):

    module = get_module(symbol_table, mock=mock_getmodule)
    orig_foo_id = id(module.foo)
    orig_bar_id = id(module.bar)

    # When:
    configure({
        "foo": {
            "parameter": "foo_param"
        }
    })

    # Then:
    assert module.foo.__name__ == 'foo'
    assert id(module.foo) != orig_foo_id
    assert hasattr(module.foo, "__wrapped__")
    assert id(module.foo.__wrapped__) == orig_foo_id

    assert module.bar.__name__ == 'bar'
    assert id(module.bar) == orig_bar_id
    assert not(hasattr(module.bar, "__wrapped__"))

@mock.patch("src.pyfunctrack.core.inspect.getmodule")
def test_instance_method_wrapping(mock_getmodule, symbol_table):

    # Given:
    module = get_module(symbol_table, mock=mock_getmodule)
    orig_red_dog_id = id(module.red_dog)
    orig_red_dog_bark_id = id(module.red_dog.bark)

    # When:
    configure({
        "red_dog.bark": {
            "parameter": "bark_param"
        }
    })

    # Then:
    assert id(module.red_dog.bark) != orig_red_dog_bark_id
    assert id(module.red_dog) == orig_red_dog_id