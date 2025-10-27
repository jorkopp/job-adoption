"""
Scrapes two animal shelters (HWAC and RCHS), filters for allowed breeds and female dogs.
Sends SMS via Twilio for each new match, and updates notified.json so that we don't send duplicate notifications.
Designed to run in GitHub Actions as a scheduled job (e.g., every day at 11:00 AM).
"""
import re
import requests
from bs4 import BeautifulSoup

from config import Config
from animal_shelter import AnimalShelter

class Scraper:
    USER_AGENT = "Mozilla/5.0 (compatible; DogAlertBot/1.0; +https://github.com/sfierro/dog-adoption)"
    
    @staticmethod
    def scrape_dogs(animal_shelter):
        print(f"Scraping dogs from {animal_shelter.name()}...")
        r = Scraper._http_get(animal_shelter.url())
        print(f"HTTP GET response: {r}")

        if not r:
            return []

        soup = BeautifulSoup(r.text, "html.parser")
        return animal_shelter.scrape_dogs(soup)

    @staticmethod
    def filter_adoptable_dogs(dogs):
        adoptable_dogs = []
        for dog in dogs:
            if dog.sex.lower() != Config.SEX:
                continue
            if float(dog.weight) > Config.MAX_WEIGHT:
                continue
            # Convert age to float for comparison, but keep original text in dog.age
            age_in_years = float(AnimalShelter._parse_age(dog.age))
            if age_in_years > Config.MAX_AGE:
                continue
            breed_allowed = False
            for breed in Config.ALLOWED_BREEDS:
                if breed in dog.breed.lower():
                    breed_allowed = True
            if not breed_allowed:
                continue
            adoptable_dogs.append(dog)
        return adoptable_dogs

    # --- Utilities ---

    @staticmethod
    def _http_get(url, **kwargs):
        headers = kwargs.pop("headers", {})
        headers.setdefault("User-Agent", Scraper.USER_AGENT)
        try:
            r = requests.get(url, headers=headers, timeout=15)
            r.raise_for_status()
            return r
        except Exception:
            return None

    @staticmethod
    def _normalize_text(t: str):
        if not t:
            return ""
        return re.sub(r"\s+", " ", t).strip().lower()