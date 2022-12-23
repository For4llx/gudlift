import pytest
from flask import template_rendered
from contextlib import contextmanager
from server import create_app

@contextmanager
def captured_templates():
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record)

@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client

@pytest.fixture
def club():
    return {
        "name":"Simply Lift",
        "email":"john@simplylift.co",
        "points": 13,
    }


@pytest.fixture
def clubs():
    return [
    {
        "name":"Simply Lift",
        "email":"john@simplylift.co",
        "points": 13
    },
    {
        "name":"Iron Temple",
        "email": "admin@irontemple.com",
        "points": 4
    },
    {   "name":"She Lifts",
        "email": "kate@shelifts.co.uk",
        "points": 12
    }
]

@pytest.fixture
def competition():
    return {
        "name": "Spring Festival",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": 25
    }

@pytest.fixture
def competitions():
    return [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": 25
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": 13
        }
    ]