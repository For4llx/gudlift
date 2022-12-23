from tests.conftest import client, club, competitions, competition, captured_templates, clubs
from flask import url_for
from club import Club
import server
import json
from dataclasses import dataclass


@dataclass
class MockClub:
    name: str
    email: str
    points: int
    places_booked = {}
    
    def data(self):
        data = {
            "name": self.name,
            "email": self.email,
            "points": self.points,
            "places_booked": self.places_booked
        }
        return data

    def remove_points(self, places_required: int):
        self.points -= places_required

    def add_places_to_competition(self, places_required: int, competition_name: str):
        self.places_booked[competition_name] += places_required

    def save(self, clubs: list, index: int):
        clubs[index] = self.data()
        serialized_clubs = json.dumps({"clubs" : clubs})
        with open('clubs.json', "w") as file:
            file.write(serialized_clubs)


@dataclass
class MockCompetition:
    name: str
    date: str
    numberOfPlaces: int
    max_places_required: int = 12
    
    def data(self):
        data = {
            "name": self.name,
            "date": self.date,
            "numberOfPlaces": self.numberOfPlaces,
            "max_places_required": self.max_places_required
        }
        return data

    def remove_places(self, places_required:int):
        self.numberOfPlaces -= places_required

    def save(self, competitions: list, index: int):
        competitions[index] = self.data()
        serialized_compettions = json.dumps({"competitions" : competitions})
        with open('competitions.json', "w") as file:
            file.write(serialized_compettions)


def test_index(client):
    """Should give 200 code and the index page"""
    with captured_templates() as templates:
        response = client.get('/')
        template, context = templates[0]
        assert response.status_code == 200
        assert template.name == 'index.html'

def test_showSummary(client, mocker, club, clubs, competitions):
    """Should give 200 code and the welcome page with the correct context"""
    with captured_templates() as templates:
        mocker.patch.object(server, 'clubs', clubs)
        mocker.patch.object(server, 'competitions', competitions)
        email = club['email']
        response = client.post('/showSummary', data={'email': email})
        template, context = templates[0]
        assert response.status_code == 200
        assert template.name == 'welcome.html'
        assert context['club'] == club
        assert context['competitions'] == competitions

def test_book(client, mocker, club, competitions, clubs):
    """Should give 200 code and the booking page with the correct context"""
    with captured_templates() as templates:
        mocker.patch.object(server, 'clubs', clubs)
        mocker.patch.object(server, 'competitions', competitions)
        club_name = club['name']
        competition = competitions[0]
        competition_name = competition['name']
        response = client.get(f'/book/{competition_name}/{club_name}')
        template, context = templates[0]
        assert response.status_code == 200
        assert template.name == 'booking.html'
        assert context['club'] == club
        assert context['competition'] == competition

def test_logout(client):
    """Should give 302 and redirect to index page"""
    response = client.get('/logout')
    assert response.status_code == 302
    assert response.location == url_for('index')

def test_purchasePlaces_not_enough_points(client, mocker, club, clubs, competitions, competition):
    """
    Should give 200 code,
    return the welcome page,
    club should not get any places,
    club shoud not get any points removed,
    competition should not get any places removed,
    error message telling the user he don't have enough points
    """
    with captured_templates() as templates:
        club['points'] = 1
        mocker.patch.object(server, 'clubs', clubs)
        mocker.patch.object(server, 'competitions', competitions)
        mocker.patch('server.Club', return_value=MockClub(**club))
        mocker.patch('server.Competition', return_value=MockCompetition(**competition))
        competition_name = competition['name']
        club_name = club['name']
        place_required = "2"
        excpeted_club = {
            'name': 'Simply Lift',
            'email': 'john@simplylift.co',
            'points': 1,
            'places_booked': {'Spring Festival': 0}
        }
        data = {
            'club': club_name,
            'competition': competition_name,
            'places': place_required
        }
        response = client.post('/purchasePlaces', data=data)
        template, context = templates[0]
        assert response.status_code == 200
        assert template.name == 'welcome.html'
        assert "Sorry, you don&#39;t have enough points." in response.data.decode()
        assert context['club'].data() == excpeted_club
        assert context['competitions'] == competitions

def test_purchasePlaces_more_place_than_available(client, mocker, club, clubs, competitions, competition):
    """
    Should give 200 code,
    return the welcome page,
    club should not get any places,
    club shoud not get any points removed,
    competition should not get any places removed,
    error message telling the user that he required more place than available
    """
    with captured_templates() as templates:
        competition['numberOfPlaces'] = 1
        mocker.patch.object(server, 'clubs', clubs)
        mocker.patch.object(server, 'competitions', competitions)
        mocker.patch('server.Club', return_value=MockClub(**club))
        mocker.patch('server.Competition', return_value=MockCompetition(**competition))
        competition_name = competition['name']
        club_name = club['name']
        place_required = "2"
        excpeted_club = {
            'name': 'Simply Lift',
            'email': 'john@simplylift.co',
            'points': 13,
            'places_booked': {'Spring Festival': 0}
        }
        data = {
            'club': club_name,
            'competition': competition_name,
            'places': place_required
        }
        response = client.post('/purchasePlaces', data=data)
        template, context = templates[0]
        assert response.status_code == 200
        assert template.name == 'welcome.html'
        assert "Sorry, you have selected more places than available." in response.data.decode()
        assert context['club'].data() == excpeted_club
        assert context['competitions'] == competitions

def test_purchasePlaces_place_required_over_maximum(client, mocker, club, clubs, competitions, competition):
    """
    Should give 200 code,
    return the welcome page,
    club should not get any places,
    club shoud not get any points removed,
    competition should not get any places removed,
    error message telling the user that he can't book more than 12 places
    """
    with captured_templates() as templates:
        mocker.patch.object(server, 'clubs', clubs)
        mocker.patch.object(server, 'competitions', competitions)
        mocker.patch('server.Club', return_value=MockClub(**club))
        mocker.patch('server.Competition', return_value=MockCompetition(**competition))
        competition_name = competition['name']
        club_name = club['name']
        place_required = "13"
        excpeted_club = {
            'name': 'Simply Lift',
            'email': 'john@simplylift.co',
            'points': 13,
            'places_booked': {'Spring Festival': 0}
        }
        data = {
            'club': club_name,
            'competition': competition_name,
            'places': place_required
        }
        response = client.post('/purchasePlaces', data=data)
        template, context = templates[0]
        assert response.status_code == 200
        assert template.name == 'welcome.html'
        assert "Sorry, you can&#39;t book more than 12 places for this competition" in response.data.decode()
        assert context['club'].data() == excpeted_club
        assert context['competitions'] == competitions


def test_purchasePlaces_is_successful(client, mocker, club, clubs, competitions, competition):
    """
    Should give 200 code,
    return the welcome page,
    club should get required places,
    club should get his points removed equal to the number of place required,
    competition should get his places removed equal to the number of place required,
    success message reminding the user the number of place required he booked and to which competition
    """
    with captured_templates() as templates:
        mocker.patch.object(server, 'clubs', clubs)
        mocker.patch.object(server, 'competitions', competitions)
        mocker.patch('server.Club', return_value=MockClub(**club))
        mocker.patch('server.Competition', return_value=MockCompetition(**competition))
        competition_name = competition['name']
        club_name = club['name']
        place_required = "1"
        excpeted_club = {
            'name': 'Simply Lift',
            'email': 'john@simplylift.co',
            'points': 12,
            'places_booked': {'Spring Festival': 1}
        }
        data = {
            'club': club_name,
            'competition': competition_name,
            'places': place_required
        }
        response = client.post('/purchasePlaces', data=data)
        template, context = templates[0]
        assert response.status_code == 200
        assert template.name == 'welcome.html'
        assert f'You have successfully booked {place_required} places for the {competition_name}' in response.data.decode()
        assert context['club'].data() == excpeted_club
        assert context['competitions'] == competitions
