import json

import pytest
import requests


def pytest_addoption(parser):
    parser.addoption("--url", action="store", default="https://ya.ru")
    parser.addoption("--status_code", action="store", type=int, default=200)

@pytest.fixture
def url(request):
    return request.config.getoption("--url")

@pytest.fixture
def status_code(request):
    return request.config.getoption("--status_code")


PATCH_URL = "https://jsonplaceholder.typicode.com/posts/100"
@pytest.fixture(scope="module")
def patch_post():
    payload = {"title": "test_Zakhvatov_patch"}
    headers = {'Content-type': 'application/json; charset=UTF-8'}
    response = requests.patch(PATCH_URL, data=json.dumps(payload),
                              headers=headers)
    yield response
    requests.delete(PATCH_URL, headers=headers)