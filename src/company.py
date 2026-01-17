from abc import abstractmethod
import re
import requests
from bs4 import BeautifulSoup
from src.job import Job

class Company:
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def url(self):
        pass

    @abstractmethod
    def scrape_jobs(self):
        """Parse the job site and return a list of Job objects"""
        pass

    @staticmethod
    def requires_excessive_experience(qualifications):
        """
        Returns True if qualifications mention 4–10+ years of experience.
        """
        if not qualifications:
            return False

        text = " ".join(qualifications).lower()

        pattern = r"\b([4-9]|10)\+?\s*(years|yrs)\b"
        return re.search(pattern, text) is not None

    @staticmethod
    def all_companies():
        return [Viasat()]

class Viasat(Company):
    def name(self):
        return "Viasat"

    #TODO: add multiple searches for different locations/keywords
    def url(self):
        return "https://careers.viasat.com/jobs?keywords=devops&stretchUnit=MILES&stretch=10&location=Carlsbad,%20CA&woe=7&regionCode=US"

    def scrape_jobs(self):
        url = "https://careers.viasat.com/api/jobs"

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            ),
            "Accept": "application/json",
        }

        jobs = []
        page = 1
        limit = 100

        while True:
            response = requests.get(
                url,
                headers=headers,
                params={"page": page, "limit": limit},
                timeout=15,
            )
            response.raise_for_status()

            data = response.json()
            page_jobs = data.get("jobs", [])

            if not page_jobs:
                break  # ✅ no more results

            for item in page_jobs:
                job_data = item.get("data", {})
                title = job_data.get("title", "").lower()

                # Location filter
                if job_data.get("location_name") != "Carlsbad":
                    continue

                # Keyword filter
                if not ("software" in title or "devops" in title):
                    continue
                
                qualifications = self._extract_qualifications(job_data)

                # Qualifications filter
                # if self.requires_excessive_experience(qualifications):
                #     continue

                jobs.append(Job(
                    company=self.name(),
                    title=job_data.get("title"),
                    req_id=job_data.get("req_id"),
                    url=job_data.get("meta_data", {}).get("canonical_url"),
                    qualifications=qualifications,
                ))

            page += 1

        return jobs
        
    def _extract_qualifications(self, job_data):
        """
        Extract bullet points under 'What you'll need'
        """
        raw = (
            job_data.get("description")
            or job_data.get("description_html")
            or ""
        )

        if not raw:
            return []

        # Convert HTML → text if needed
        if "<" in raw:
            raw = BeautifulSoup(raw, "html.parser").get_text("\n")

        text = re.sub(r"\r", "", raw)

        # Match section header
        match = re.search(
            r"what you(?:'| wi)ll need\s*(.*)",
            text,
            re.IGNORECASE | re.DOTALL,
        )

        if not match:
            return []

        section = match.group(1)

        # Stop at next section header
        section = re.split(
            r"\n\s*[A-Z][A-Za-z ]{3,}\n", section
        )[0]

        bullets = []
        for line in section.splitlines():
            line = line.strip("•- \t")
            if len(line) > 3:
                bullets.append(line)

        return bullets