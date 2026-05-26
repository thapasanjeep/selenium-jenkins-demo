import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()


def test_google_title(driver):
    driver.get("https://www.google.com")
    assert "Google" in driver.title


def test_google_search_box_exists(driver):
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    assert search_box.is_displayed()