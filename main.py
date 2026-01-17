from src.scraper import Scraper
from src.company import Company
from src.notification_generator import send_email
from src.database.db import NotifiedDatabase

def main():
    all_jobs = set()

    for company in Company.all_companies():
        jobs = Scraper.scrape_jobs(company)
        jobs = Scraper.filter_applicable_jobs(jobs)
        all_jobs.update(jobs)

    if not all_jobs:
        return

    previously_notified = NotifiedDatabase.load_previously_notified_jobs()

    new_jobs = all_jobs - previously_notified

    if not new_jobs:
        print("No new jobs found.")
        return

    body = "\n\n".join(job.description() for job in new_jobs)

    send_email(
        subject=f"{len(new_jobs)} New Job Matches Found",
        body=body
    )

    NotifiedDatabase.register_jobs_as_notified(new_jobs)

if __name__ == "__main__":
    main()