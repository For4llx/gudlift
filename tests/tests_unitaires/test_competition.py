from competition import Competition

class TestCompetition:
    def test_remove_places(self, competition):
        """Remove 1 place from the competition so 25-1 should give 24"""
        competition_1 = Competition(**competition)
        place_required = 1
        expected_value = 24
        competition_1.remove_places(place_required)
        assert competition_1.numberOfPlaces == expected_value
