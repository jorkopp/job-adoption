# Dog Adoption Alert System 🐕

An automated Python application that scrapes local animal shelters for adoptable dogs matching your specific criteria and sends SMS notifications via Twilio when new matches are found.

## Features

- **Multi-Shelter Support**: Scrapes dogs from multiple animal shelters
  - Helen Woodward Animal Center
  - Rancho Coastal Humane Society
- **Smart Filtering**: Only alerts you about dogs that match your preferences:
  - Female dogs only
  - Specific breeds (Maltese, Havanese, Terrier, Poodle, Doodle, Bichon)
  - Under 200 pounds
  - Under 2 years old
- **Duplicate Prevention**: Tracks previously notified dogs to avoid spam
- **SMS Notifications**: Sends text messages with dog details and photos via Twilio
- **Automated Scheduling**: Designed to run as a scheduled job (e.g., daily via GitHub Actions)

## How It Works

1. **Scraping**: The application scrapes dog listings from configured animal shelter websites
2. **Filtering**: Dogs are filtered based on your criteria (sex, breed, age, weight)
3. **Deduplication**: New dogs are compared against previously notified dogs
4. **Notification**: SMS alerts are sent for new matches, including photos
5. **Tracking**: Newly notified dogs are saved to prevent duplicate notifications

## Project Structure

```
dog-adoption/
├── main.py                 # Main entry point
├── adoptable_dog.py        # Dog data model
├── animal_shelter.py       # Abstract shelter class and implementations
├── scraper.py             # Web scraping logic and filtering
├── config.py              # Configuration settings
├── database/
│   ├── db.py              # Database operations for tracking notified dogs
│   └── notified.json      # JSON file storing previously notified dogs
└── messaging/
    ├── messenger.py       # Twilio SMS integration
    └── secrets.py         # Environment variable handling
```

## Setup

### Prerequisites

- Python 3.7+
- Twilio account and phone number
- Required Python packages (see Dependencies section)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/sfierro/dog-adoption.git
cd dog-adoption
```

2. Install dependencies:
```bash
pip install requests beautifulsoup4 twilio
```

3. Set up environment variables for Twilio:
```bash
export TWILIO_SID="your_twilio_account_sid"
export TWILIO_AUTH="your_twilio_auth_token"
export TWILIO_FROM="your_twilio_phone_number"
export MY_PHONE="your_phone_number"
```

### Configuration

Edit `config.py` to customize your dog preferences:

```python
class Config:
    SEX = "female"                    # Dog gender preference
    ALLOWED_BREEDS = [               # Breed preferences
        "maltese",
        "havanese", 
        "terrier",
        "poodle",
        "doodle",
        "bichon",
    ]
    MAX_WEIGHT = 200.0               # Maximum weight in pounds
    MAX_AGE = 2.0                    # Maximum age in years
```

## Usage

### Manual Execution

Run the script manually:
```bash
python main.py
```

### Automated Scheduling

The application is designed to run as a scheduled job. You can set it up with:

- **GitHub Actions**: Create a workflow file to run daily
- **Cron**: Set up a cron job on your server
- **Cloud Functions**: Deploy to AWS Lambda, Google Cloud Functions, etc.

### GitHub Actions Example

Create `.github/workflows/dog-alert.yml`:

```yaml
name: Dog Adoption Alert
on:
  schedule:
    - cron: '0 11 * * *'  # Run daily at 11:00 AM UTC
  workflow_dispatch:      # Allow manual triggers

jobs:
  alert:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install requests beautifulsoup4 twilio
      - name: Run dog alert
        env:
          TWILIO_SID: ${{ secrets.TWILIO_SID }}
          TWILIO_AUTH: ${{ secrets.TWILIO_AUTH }}
          TWILIO_FROM: ${{ secrets.TWILIO_FROM }}
          MY_PHONE: ${{ secrets.MY_PHONE }}
        run: python main.py
```

## Dependencies

- `requests`: HTTP requests for web scraping
- `beautifulsoup4`: HTML parsing
- `twilio`: SMS messaging service

## Adding New Shelters

To add support for additional animal shelters:

1. Create a new class inheriting from `AnimalShelter`
2. Implement the required methods: `name()`, `url()`, and `scrape_dogs(soup)`
3. Add the new shelter to `AnimalShelter.all_animal_shelters()`

Example:
```python
class NewShelter(AnimalShelter):
    def name(self):
        return "New Animal Shelter"
    
    def url(self):
        return "https://newshelter.org/dogs"
    
    def scrape_dogs(self, soup):
        # Implement parsing logic for this shelter's HTML structure
        dogs = []
        # ... parsing logic ...
        return dogs
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Feel free to use and modify for your own dog adoption needs!

## Disclaimer

This tool is for personal use to help find adoptable dogs. Please respect the animal shelters' websites and their terms of service. The application includes appropriate delays and user-agent headers to be respectful of the target websites.
