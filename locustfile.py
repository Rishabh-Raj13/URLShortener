from locust import HttpUser,task,between

class DjangoLoadTest(HttpUser):
    wait_time=between(1,3)

    @task
    def home_page(self):
        self.client.get("urlShort/")

    @task
    def short_url_redirect(self):
        self.client.get("SrUZSwDfEY")
    
