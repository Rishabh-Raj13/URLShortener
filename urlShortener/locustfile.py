from locust import HttpUser, task, between

class URLShortenerUser(HttpUser):
    wait_time = between(1, 3)  # Wait between 1-3 seconds randomly

    def on_start(self):
        """Generate a short URL once when a user starts"""
        response = self.client.post("urlShort/", json={"url": "https://www.youtube.com"})
        if response.status_code == 201:  # Assuming 201 Created
            self.short_url = response.json().get("slug")  # Adjust based on API response
        else:
            self.short_url = None

    @task
    def shorten_url(self):
        """Test shortening a URL"""
        self.client.post("urlShort/", json={"url": "https://www.youtube.com"})

    @task
    def access_shortened_url(self):
        """Test accessing a shortened URL"""
        if self.short_url:
            self.client.get(self.short_url)
