from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage

class InventoryPage(BasePage):
    """상품 목록 페이지 요소 및 동작 정의"""

    # Locators
    SORT_DROPDOWN = (By.CLASS_NAME, 'product_sort_container')
    ITEM_PRICES = (By.CLASS_NAME, 'inventory_item_price')
    ADD_TO_CART_BTNS = (By.XPATH, '//button[contains(text(), "Add to cart")]')
    CART_BADGE = (By.CLASS_NAME, 'shopping_cart_badge')
    CART_LINK = (By.CLASS_NAME, 'shopping_cart_link')

    def sort_by(self, value):
        """
        정렬 드롭다운 선택 (lohi, hilo, az, za)
        ex) lohi = Low to High
        """
        select = Select(self.find(self.SORT_DROPDOWN))
        select.select_by_value(value)
    
    def get_all_prices(self):
        """화면의 모든 상품 가격을 숫자(float) 리스트로 반환"""
        elements = self.driver.find_elements(*self.ITEM_PRICES)

        # $ 기호를 제거하고 실수형으로 변환하여 리스트 생성
        return [float(e.text.replace('$', '')) for e in elements]
    
    def add_first_item(self):
        """목록의 첫 번째 상품에 장바구니에 담기"""
        btns = self.driver.find_elements(*self.ADD_TO_CART_BTNS)

        if btns:
            btns[0].click()
    
    def get_badge_count(self):
        """장바구니 뱃지 숫자 반환 (없으면 0 리턴)"""
        try:
            # 뱃지가 있으면 숫자로 변환해서 리턴
            return int(self.get_text(self.CART_BADGE))
        
        except:
            # 뱃지가 아예 없으면(0개일 때) 에러가 나므로 0 리턴
            return 0
    
    def go_to_cart(self):
        """장바구니 아이콘 클릭하여 이동"""
        self.click(self.CART_LINK)