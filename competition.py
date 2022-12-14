from dataclasses import dataclass
import json

@dataclass
class Competition:
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
