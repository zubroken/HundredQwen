import unittest

from fastapi.testclient import TestClient
from fastapi import FastAPI

from api import home_page
from api.home_page import load_home_page_html
from api.home_routes import register_home_routes
from api.routes import create_app
from services.llm_service import LLMConfig


class HomePageTest(unittest.TestCase):
    def test_load_home_page_html_returns_embedded_constant(self):
        html = load_home_page_html()

        self.assertTrue(hasattr(home_page, "HOME_PAGE_HTML"))
        self.assertEqual(html, home_page.HOME_PAGE_HTML)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn('id="panel-chat"', html)
        self.assertIn("/api/chat-simple", html)
        self.assertIn('id="studyTimeCard"', html)
        self.assertIn("/api/study-time/", html)

    def test_root_route_returns_html_page(self):
        client = TestClient(create_app(LLMConfig(api_key="", model="deepseek-chat", base_url="")))

        response = client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])
        self.assertIn('id="panel-chat"', response.text)
        self.assertIn("/api/chat-simple", response.text)

    def test_root_route_disables_browser_cache(self):
        app = FastAPI()
        register_home_routes(app)

        response = TestClient(app).get("/")

        self.assertEqual(response.headers["cache-control"], "no-store")


if __name__ == "__main__":
    unittest.main()
