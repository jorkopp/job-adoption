from abc import abstractmethod
from src.adoptable_dog import AdoptableDog
import re

class AnimalShelter:
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def url(self):
        pass

    @abstractmethod
    def scrape_dogs(self, soup):
        """Parse the HTML soup and return a list of AdoptableDog objects"""
        pass

    @staticmethod
    def _parse_weight(weight_text):
        """Parse weight text that may contain fractions like '45 ½' or '45.5'"""
        if not weight_text:
            return ""
        
        # Remove 'lbs' and extra whitespace
        weight_text = re.sub(r'\blbs?\b', '', weight_text).strip()
        
        # Handle fractions
        fraction_map = {
            '½': 0.5,
            '⅓': 1/3,
            '⅔': 2/3,
            '¼': 0.25,
            '¾': 0.75,
            '⅛': 0.125,
            '⅜': 0.375,
            '⅝': 0.625,
            '⅞': 0.875
        }
        
        # Look for pattern like "45 ½" or "45½"
        match = re.search(r'(\d+)\s*([½⅓⅔¼¾⅛⅜⅝⅞])', weight_text)
        if match:
            whole_number = float(match.group(1))
            fraction = fraction_map[match.group(2)]
            return str(whole_number + fraction)
        
        # Look for decimal numbers
        match = re.search(r'(\d+\.?\d*)', weight_text)
        if match:
            return match.group(1)
        
        return weight_text

    @staticmethod
    def _parse_age(age_text):
        """Parse age text and convert to years as float"""
        if not age_text:
            return ""
        
        age_text = age_text.lower().strip()
        
        # Handle fractions
        fraction_map = {
            '½': 0.5,
            '⅓': 1/3,
            '⅔': 2/3,
            '¼': 0.25,
            '¾': 0.75,
            '⅛': 0.125,
            '⅜': 0.375,
            '⅝': 0.625,
            '⅞': 0.875
        }
        
        # Pattern for "2 years 6 months 3 weeks" (years + months + weeks)
        full_compound_match = re.search(r'(\d+)\s*years?\s*(\d+)\s*months?\s*(\d+)\s*weeks?', age_text)
        if full_compound_match:
            years = float(full_compound_match.group(1))
            months = float(full_compound_match.group(2))
            weeks = float(full_compound_match.group(3))
            total_years = years + (months / 12) + (weeks / 52)
            return str(total_years)
        
        # Pattern for "2 years 6 months" (compound age)
        compound_match = re.search(r'(\d+)\s*years?\s*(\d+)\s*months?', age_text)
        if compound_match:
            years = float(compound_match.group(1))
            months = float(compound_match.group(2))
            total_years = years + (months / 12)
            return str(total_years)
        
        # Pattern for "6 months 2 weeks" (months + weeks)
        months_weeks_match = re.search(r'(\d+)\s*months?\s*(\d+)\s*weeks?', age_text)
        if months_weeks_match:
            months = float(months_weeks_match.group(1))
            weeks = float(months_weeks_match.group(2))
            total_years = (months / 12) + (weeks / 52)
            return str(total_years)
        
        # Pattern for "2 years 3 weeks" (years + weeks)
        years_weeks_match = re.search(r'(\d+)\s*years?\s*(\d+)\s*weeks?', age_text)
        if years_weeks_match:
            years = float(years_weeks_match.group(1))
            weeks = float(years_weeks_match.group(2))
            total_years = years + (weeks / 52)
            return str(total_years)
        
        # Pattern for "5 ½ years" or "5½ years"
        years_match = re.search(r'(\d+)\s*([½⅓⅔¼¾⅛⅜⅝⅞]?)\s*years?', age_text)
        if years_match:
            whole_years = float(years_match.group(1))
            fraction_char = years_match.group(2)
            if fraction_char:
                fraction = fraction_map[fraction_char]
                return str(whole_years + fraction)
            return str(whole_years)
        
        # Pattern for "18 months" or "4 months"
        months_match = re.search(r'(\d+)\s*months?', age_text)
        if months_match:
            months = float(months_match.group(1))
            years = months / 12
            return str(years)
        
        # Pattern for "10 weeks" or "15 weeks"
        weeks_match = re.search(r'(\d+)\s*weeks?', age_text)
        if weeks_match:
            weeks = float(weeks_match.group(1))
            years = weeks / 52
            return str(years)
        
        # Pattern for "6 months" (without "months" word)
        months_only_match = re.search(r'(\d+)\s*months?', age_text)
        if months_only_match:
            months = float(months_only_match.group(1))
            years = months / 12
            return str(years)
        
        # If no pattern matches, return original text
        return age_text

    @staticmethod
    def all_animal_shelters():
        return [HelenWoodwardAnimalCenter(), RanchoCoastalHumaneSociety()]

class HelenWoodwardAnimalCenter(AnimalShelter):
    def name(self):
        return "Helen Woodward Animal Center"

    def url(self):
        return "https://animalcenter.org/pet-adoption/adoptable-dogs/"

    def scrape_dogs(self, soup):
        """Scrape Helen Woodward Animal Center format"""
        dogs = []
        
        # Find all product content divs
        for content_div in soup.find_all('div', class_='product_content'):
            # Get name from h3
            name_h3 = content_div.find('h3', class_='modal-title')
            if not name_h3:
                continue
                
            name = name_h3.text.strip()
            
            # Get image from previous sibling (product_img div)
            image = ""
            prev_sibling = content_div.find_previous_sibling()
            if prev_sibling and prev_sibling.get('class') and 'product_img' in prev_sibling.get('class'):
                img_tag = prev_sibling.find('img')
                if img_tag and img_tag.get('src'):
                    image = img_tag.get('src')
            
            # Get breed from h4
            breed_h4 = content_div.find('h4', class_='span-desc')
            breed = breed_h4.text.strip() if breed_h4 else ""
            
            # Get sex, age, weight from ul/li structure
            sex = ""
            age = ""
            weight = ""
            
            ul = content_div.find('ul')
            if ul:
                for li in ul.find_all('li', class_='class-li'):
                    heading_span = li.find('span', class_='span-heading')
                    text_span = li.find('span', class_='span-text')
                    
                    if heading_span and text_span:
                        heading = heading_span.text.strip().lower()
                        text = text_span.text.strip()
                        
                        if 'sex' in heading:
                            sex = text.lower()
                            sex = sex.replace(" - Spayed", "").strip()
                            sex = sex.replace(" - Neutered", "").strip()
                        elif 'age' in heading:
                            age = text
                        elif 'weight' in heading:
                            weight = AnimalShelter._parse_weight(text)
            
            # Only add dogs that have breed information (skip empty duplicates)
            if breed.strip():
                dog = AdoptableDog(self.name(), name, breed, sex, age, weight, image, self.url())
                dogs.append(dog)
        
        return dogs

class RanchoCoastalHumaneSociety(AnimalShelter):
    def name(self):
        return "Rancho Coastal Humane Society"

    def url(self):
        return "https://rchumanesociety.org/dogs-for-adoption/"

    def scrape_dogs(self, soup):
        """Scrape Rancho Coastal Humane Society format"""
        dogs = []
        
        # Find all articles with dog listings
        for article in soup.find_all('article', class_=lambda x: x and 'post' in x):
            # Get name from h2 with link
            name_h2 = article.find('h2', class_='entry-title')
            if not name_h2:
                continue
                
            name_link = name_h2.find('a')
            if not name_link:
                continue
                
            name = name_link.text.strip()
            
            # Get image from post-thumbnail
            image = ""
            thumbnail = article.find('div', class_='post-thumbnail')
            if thumbnail:
                img_tag = thumbnail.find('img')
                if img_tag and img_tag.get('src'):
                    image = img_tag.get('src')
            
            # Get breed, sex, age, weight from entry-content text
            entry_content = article.find('div', class_='entry-content')
            if entry_content:
                # Get the text content after the h2
                content_text = entry_content.get_text()
                lines = [line.strip() for line in content_text.split('\n') if line.strip()]
                
                # Find the line with the name and get subsequent lines
                breed = ""
                sex = ""
                age = ""
                weight = ""
                
                for i, line in enumerate(lines):
                    if name.lower() in line.lower():
                        # Get the next few lines for breed, sex, age, weight
                        if i + 1 < len(lines):
                            breed = lines[i + 1]
                        if i + 2 < len(lines):
                            sex = lines[i + 2]
                        if i + 3 < len(lines):
                            age = lines[i + 3]
                        if i + 4 < len(lines):
                            weight = AnimalShelter._parse_weight(lines[i + 4])
                        break
            
            dog = AdoptableDog(self.name(), name, breed, sex, age, weight, image, self.url())
            dogs.append(dog)
        
        return dogs