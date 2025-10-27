from animal_shelter import AnimalShelter
from database.db import NotifiedDatabase
from messaging.messenger import Messenger
from scraper import Scraper

if __name__ == '__main__':
    previously_notified_dogs = NotifiedDatabase.load_previously_notified_dogs()

    dogs = []
    for animal_shelter in AnimalShelter.all_animal_shelters():
        animal_shelter_dogs = Scraper.scrape_dogs(animal_shelter)
        print(f"{animal_shelter.name()} dogs: {len(animal_shelter_dogs)}")
        dogs.extend(animal_shelter_dogs)

    print(f"Dogs: {[dog.description() for dog in dogs]}")
    adoptable_dogs = Scraper.filter_adoptable_dogs(dogs)
    print(f"Total adoptable dogs: {len(adoptable_dogs)}")

    new_adoptable_dogs = [dog for dog in adoptable_dogs if dog not in previously_notified_dogs]
    print(f"New adoptable dogs: {len(new_adoptable_dogs)}")
    Messenger.send_notifications(new_adoptable_dogs)
    NotifiedDatabase.register_dogs_as_notified(new_adoptable_dogs)