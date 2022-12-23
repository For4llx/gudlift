from club import Club
from competition import Competition
from tests.conftest import club, competition
import json


class MockClub:
    def __init__(self, name:str, email:str, points:str, places_booked={}):
        self.name = name
        self.email = email
        self.points = points
        self.places_booked = places_booked

    def data(self):
        data = {
            "name": self.name,
            "email": self.email,
            "points": self.points,
            "places_booked": self.places_booked
        }
        return data

    def remove_points(self, places_required:int):
        self.points -= places_required

    def add_places_to_competition(self, places_required:int, competition_name:str):
        self.places_booked[competition_name] += places_required

    def save(self, clubs, index):
        clubs[index] = self.data()
        serialized_clubs = json.dumps({"clubs" : clubs})
        with open('clubs.json', "w") as file:
            file.write(serialized_clubs)


class TestClub:
    def test_data(self, club):
        """Check if data return dict object with correct value"""
        club_1 = Club(**club)
        expected = {'name': 'Simply Lift', 'email': 'john@simplylift.co', 'points': 13, 'places_booked': {}}
        assert club_1.data() == expected

    def test_remove_points(self, club):
        """Remove one point from the club (13-1 should give 12)"""
        club_1 = Club(**club)
        place_required = 1
        expected_value = 12

        club_1.remove_points(place_required)
        assert club_1.points == expected_value

    def test_add_places_to_competition(self, club, competition):
        """
        If this is the first time the club book in the competition,
        should initiate the key "competition_name:value" in the dict "places booked" to 0 and add the place required to it
        (0 + 1 should give 1)
        else it should just add the place required (2 + 1 should give 3)
        """
        club_1 = Club(**club)
        competition_1 = Competition(**competition)
        place_required = 1
        expected_value = 1
        if not competition_1.name in club_1.places_booked:
            club_1.places_booked[competition_1.name] = 0

        club_1.add_places_to_competition(place_required, competition_1.name)
        assert club_1.places_booked[competition_1.name] == expected_value

        place_required = 2
        expected_value = 3
        club_1.add_places_to_competition(place_required, competition_1.name)
        assert club_1.places_booked[competition_1.name] == expected_value
