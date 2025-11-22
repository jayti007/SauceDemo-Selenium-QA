from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    USERNAME = (By.ID, 'user-name')
    PASSWORD = (By.ID, 'password')
    LOGIN_BTN = (By.ID, 'login-button') 
    ERROR_MSG = (By.CSS_SELECTOR, '[data-test="error"]')    

    def login(self, username, password):
        """아이디/비번 입력하고 로그인 버튼 클릭"""
        self.input_text(self.USERNAME, username)
        self.input_text(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)
    
    def get_error_message(self):
        """에러 메시지 텍스트 반환"""
        return self.get_text(self.ERROR_MSG)

