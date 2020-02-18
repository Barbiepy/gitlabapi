"""Test searching Gitlab projects."""

import requests
from pytest_bdd import scenario, given, then, parsers


GITLAB_URL = 'https://gitlab.com/api/v4/projects/?search={}'


@scenario('../features/gitlab.feature', 'got not empty list of projects')
def test_gitlab():
    pass


@given(parsers.parse('user pass a <substring> to endpoint'))
def gitlab_request(substring):
    assert isinstance(substring, str)
    return requests.get(GITLAB_URL.format(substring))


@then(parsers.parse('server returns next <number> of projects'))
def gitlab_repsonse(gitlab_request, number):
    response = gitlab_request.json()
    assert len(response) == int(number)
