from src.scraper import Scraper
from src.company import Company
from src.emailer import send_email

def main():
    all_jobs = set()

    for company in Company.all_companies():
        jobs = Scraper.scrape_jobs(company)
        jobs = Scraper.filter_applicable_jobs(jobs)
        all_jobs.update(jobs)

    if not all_jobs:
        return

    body = "\n\n".join(job.description() for job in all_jobs)

    send_email(
        subject="New Job Matches Found",
        body=body
    )

if __name__ == "__main__":
    main()