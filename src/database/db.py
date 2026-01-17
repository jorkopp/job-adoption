import json
from src.job import Job

class NotifiedDatabase:
    PATH = "src/database/notified.json"

    @staticmethod
    def load_previously_notified_jobs():
        try:
            with open(NotifiedDatabase.PATH, "r") as f:
                data = json.load(f)
                jobs = set()
                for job_data in data:
                    # Reconstruct Job objects from JSON
                    job = Job(
                        company=job_data['company'],
                        title=job_data['title'],
                        req_id=job_data['req_id'],
                        url=job_data['url']
                    )
                    jobs.add(job)
                return jobs
        except Exception:
            return set([])

    @staticmethod
    def register_jobs_as_notified(jobs):
        data = NotifiedDatabase.load_previously_notified_jobs()
        for job in jobs:
            data.add(job)
        with open(NotifiedDatabase.PATH, "w") as f:
            # Convert Job objects to dictionaries for JSON serialization
            jobs_list = []
            for job in data:
                jobs_list.append({
                    'company': job.company,
                    'title': job.title,
                    'req_id': job.req_id,
                    'url': job.url
                })
            json.dump(jobs_list, f, indent=2)