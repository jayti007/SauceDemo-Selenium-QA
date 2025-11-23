from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    """결제(Checkout) 페이지 요소 및 동작 정의"""

    FIRST_NAME = (By.ID, 'first-name')
    LAST_NAME = (By.ID, 'last-name')
    ZIP_CODE = (By.ID, 'postal-code')
    CONTINUE_BTN = (By.ID, 'continue')
    ERROR_MSG = (By.CSS_SELECTOR, '[data-test="error"]')

    ITEM_TOTAL = (By.CLASS_NAME, 'summary_subtotal_label')
    TAX_LABEL = (By.CLASS_NAME, 'summary_tax_label')
    TOTAL_LABEL = (By.CLASS_NAME, 'summary_total_label')
    FINISH_BTN = (By.ID, 'finish')
    COMPLETE_HEADER = (By.CLASS_NAME, 'complete-header')
    
    def fill_info(self, first, last, zip_code):
        """배송 정보 3가지 입력 후 Continue 클릭"""
        self.input_text(self.FIRST_NAME, first)
        self.input_text(self.LAST_NAME, last)
        self.input_text(self.ZIP_CODE, zip_code)
        self.click(self.CONTINUE_BTN)
    
    def get_error_message(self):
        """에러 메시지 텍스트 반환"""
        return self.get_text(self.ERROR_MSG)
    
    def get_prices(self):
        """
        화면의 가격 텍스트들을 가져와서 숫자로 변환해 반환
        ex) 'Item total: $29.99' -> 29.99 (float)
        """
        item_text = self.get_text(self.ITEM_TOTAL)
        tax_text = self.get_text(self.TAX_LABEL)
        total_text = self.get_text(self.TOTAL_LABEL)
        
        item = float(item_text.split('$')[1])
        tax = float(tax_text.split('$')[1])
        total = float(total_text.split('$')[1])

        return item, tax, total

    def finish_order(self):
        """최종 결제 완료(Finish) 버튼 클릭"""
        self.click(self.FINISH_BTN)
    
    def get_complete_message(self):
        """주문 완료 화면의 큰 제목('THANK YOU...') 반환"""
        return self.get_text(self.COMPLETE_HEADER)