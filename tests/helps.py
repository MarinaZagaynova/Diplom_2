import random

import requests

from tests.data import password, name
from tests.endpoints import Endpoints


def get_token():
    response = success_registration()
    answer = response.json()
    access_token = answer.get('accessToken')
    return access_token


def get_ingredients():
    response = requests.get(Endpoints.url + Endpoints.ingredients)
    return [ingredient["_id"] for ingredient in response.json()["data"]]


def success_registration():
    payload = {
        "email": f"new{random.randint(1, 100000)}@gmail.com",
        "password": password,
        "name": name}
    return requests.post(Endpoints.url + Endpoints.registration, json=payload)
