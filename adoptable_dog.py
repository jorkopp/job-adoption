class AdoptableDog:
    def __init__(self, shelter, name, breed, sex, age, weight, image, url):
        self.shelter = shelter
        self.name = name
        self.breed = breed
        self.sex = sex
        self.age = age
        self.weight = weight
        self.image = image
        self.url = url

    def description(self):
        return f"{self.name}, {self.sex}, {self.age}, {self.breed}, {self.weight} pounds."
    
    def __eq__(self, other):
        if not isinstance(other, AdoptableDog):
            return False
        return (self.shelter == other.shelter and 
                self.name == other.name and 
                self.breed == other.breed and 
                self.sex == other.sex and 
                self.age == other.age and 
                self.weight == other.weight and 
                self.url == other.url)
    
    def __hash__(self):
        return hash((self.shelter, self.name, self.breed, self.sex, self.age, self.weight, self.url))