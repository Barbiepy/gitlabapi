"""A simple BDD-test for test function."""

from pytest_bdd import scenario, given, then, parsers
from run import hello


@scenario('../features/hello.feature', 'user got a message to console')
def test_hello():
    pass


@given(parsers.parse('user pass a <message> to argument'))
def hello_response(message):
    assert isinstance(message, str)


@then(parsers.parse('user see a <message> in console'))
def hello_console(message, capsys):
    hello(message)
    out, err = capsys.readouterr()

    assert not err
    assert out.rstrip() == message
