import unittest
import os

os.environ["TESTING"] = "true"

from src.app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        print(response.status_code)
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>MLH Fellow</title>" in html
        # TODO Add more tests relating to the home page
        assert (
            '<div id="team" class="team-section">' in html
        )  # check if team cards are present since they are inserted as a component at the home page.

    def test_timeline(self):
        print('here')
        response = self.client.get("/api/timeline_post")
        
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0
        # TODO Add more tests relating to the /api/timeline_post GET and POST apis
        # Create a new user, verify the response status code
        response2 = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "content": "Some sample data here",
            },
        )
        assert response2.status_code == 200
        # Verify that the new user is returned by the get method
        response3 = self.client.get("/api/timeline_post")
        json2 = response3.get_json()
        assert len(json2["timeline_posts"]) == 1
        # TODO Add more tests relating to the timeline page
        # Check timeline page status code
        response4 = self.client.get("/timeline/")
        print(response4.status_code)
        assert response4.status_code == 200
        html = response4.get_data(as_text=True)
        assert "<title>Timeline</title>" in html

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post(
            "/api/timeline_post",
            data={"email": "john@example.com", "content": "Hello world, I'm John!"},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post(
            "/api/timeline_post",
            data={"name": "John Doe", "email": "john@example.com", "content": ""},
        )
        print(response.status_code)
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "not-an-email",
                "content": "Hello world, I'm John!",
            },
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
