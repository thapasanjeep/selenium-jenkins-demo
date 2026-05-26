import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.google_page import GooglePage


import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

def test_google_homepage_title(driver):
    google_page = GooglePage(driver)
    google_page.open_google()

    assert "Google" in google_page.get_title()


def test_google_search_box_is_visible(driver):
    google_page = GooglePage(driver)
    google_page.open_google()

    assert google_page.is_search_box_visible()