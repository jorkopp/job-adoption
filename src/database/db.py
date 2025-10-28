import json
from src.adoptable_dog import AdoptableDog

class NotifiedDatabase:
    PATH = "src/database/notified.json"

    @staticmethod
    def load_previously_notified_dogs():
        try:
            with open(NotifiedDatabase.PATH, "r") as f:
                data = json.load(f)
                dogs = set()
                for dog_data in data:
                    # Reconstruct AdoptableDog objects from JSON
                    dog = AdoptableDog(
                        shelter=dog_data['shelter'],
                        name=dog_data['name'],
                        breed=dog_data['breed'],
                        sex=dog_data['sex'],
                        age=dog_data['age'],
                        weight=dog_data['weight'],
                        image=dog_data['image'],
                        url=dog_data['url']
                    )
                    dogs.add(dog)
                return dogs
        except Exception:
            return set([])

    @staticmethod
    def register_dogs_as_notified(adoptable_dogs):
        data = NotifiedDatabase.load_previously_notified_dogs()
        for adoptable_dog in adoptable_dogs:
            data.add(adoptable_dog)
        with open(NotifiedDatabase.PATH, "w") as f:
            # Convert AdoptableDog objects to dictionaries for JSON serialization
            dogs_list = []
            for dog in data:
                dogs_list.append({
                    'shelter': dog.shelter,
                    'name': dog.name,
                    'breed': dog.breed,
                    'sex': dog.sex,
                    'age': dog.age,
                    'weight': dog.weight,
                    'image': dog.image,
                    'url': dog.url
                })
            json.dump(dogs_list, f, indent=2)
