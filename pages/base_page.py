from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """모든 페이지 객체가 상속받는 부모 클래스"""

    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10

    def find(self, locator):
        """요소가 화면에 나타날 때까지 대기 (Explicit Wait)"""

        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def click(self, locator):
        """요소를 찾아서 클릭"""
        element = self.find(locator)
        element.click()

    def input_text(self, locator, text):
        """요소를 찾아서 텍스트를 입력"""
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """요소의 텍스트를 가져오기"""
        return self.find(locator).text
