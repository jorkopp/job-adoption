"""
Scrapes job postings from company career pages and notifies users of new listings.
"""
import re
import requests
from bs4 import BeautifulSoup

from src.config import Config
from src.company import Company

class Scraper:
    USER_AGENT = "Mozilla/5.0 (compatible; JobAlertBot/1.0; +https://github.com/jorkopp/jo-adoption)"
    
    @staticmethod
    def scrape_jobs(company):
        r = Scraper._http_get(company.url())  

        if not r:
            return []

        return company.scrape_jobs()

    @staticmethod
    def filter_applicable_jobs(jobs):
        applicable_jobs = []
        for job in jobs:
            job_applicable = True
            for keyword in Config.BLOCKLIST:
                if keyword in job.title.lower():
                    job_applicable = False
            if not job_applicable:
                continue
            applicable_jobs.append(job)
        return applicable_jobs

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