class Job:
    def __init__(self, company, title, url, req_id, qualifications=None):
        self.company = company
        self.title = title
        self.url = url
        self.req_id = req_id
        self.qualifications = qualifications or []

#TODO: make link clickable?
    def description(self):
        quals = ""
        if self.qualifications:
            quals = "\n Qualifications:\n" + "\n".join(
                f"  - {q}" for q in self.qualifications
            )
        return (
            f"{self.company}: {self.title}\n"
            f" Req ID: {self.req_id}\n"
            f" URL: {self.url}"
            f"{quals}"
        )
    
    def __eq__(self, other):
        if not isinstance(other, Job):
            return False
        return (self.company == other.company and
                self.req_id == other.req_id)
    
    def __hash__(self):
        return hash((self.company, self.req_id))