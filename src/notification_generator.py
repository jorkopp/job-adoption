from src.animal_shelter import AnimalShelter
from src.database.db import NotifiedDatabase
from src.messaging.messenger import Messenger
from src.scraper import Scraper

class NotificationGenerator:
    
    @staticmethod
    def run():
        previously_notified_dogs = NotifiedDatabase.load_previously_notified_dogs()

        dogs = []
        for animal_shelter in AnimalShelter.all_animal_shelters():
            animal_shelter_dogs = Scraper.scrape_dogs(animal_shelter)
            dogs.extend(animal_shelter_dogs)

        adoptable_dogs = Scraper.filter_adoptable_dogs(dogs)

        new_adoptable_dogs = [dog for dog in adoptable_dogs if dog not in previously_notified_dogs]
        
        print(f"\nFound {len(new_adoptable_dogs)} new adoptable dog{'' if len(new_adoptable_dogs) == 1 else 's'}{'.' if len(new_adoptable_dogs) == 0 else ':'}")
        for dog in new_adoptable_dogs:
            print(f"\n\t{dog.description()}")
        print("\n")

        Messenger.send_notifications(new_adoptable_dogs)
        NotifiedDatabase.register_dogs_as_notified(new_adoptable_dogs)