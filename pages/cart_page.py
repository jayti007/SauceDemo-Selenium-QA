from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    """장바구니 페이지 요소 및 동작 정의"""
    
    # Locators
    CHECKOUT_BTN = (By.ID, 'checkout')
    
    def click_checkout(self):
        """체크아웃 버튼 클릭해서 결제 화면으로 이동"""
        self.click(self.CHECKOUT_BTN)