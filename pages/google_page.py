from selenium.webdriver.common.by import By


class GooglePage:
    SEARCH_BOX = (By.NAME, "q")

    def __init__(self, driver):
        self.driver = driver

    def open_google(self):
        self.driver.get("https://www.google.com")

    def get_title(self):
        return self.driver.title

    def is_search_box_visible(self):
        return self.driver.find_element(*self.SEARCH_BOX).is_displayed()