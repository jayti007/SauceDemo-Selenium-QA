import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

@pytest.mark.usefixtures('driver')
class TestInventory:
    """상품 목록(Inventory) 기능 관련 테스트 시나리오"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """모든 INV 테스트 전에 로그인 상태로 만듦"""
        login = LoginPage(driver)

        driver.get('https://www.saucedemo.com/')
        login.login('standard_user', 'secret_sauce')
    
    @pytest.mark.P1
    def test_inv_01_sort_price(self, driver):
        """INV-01: 가겨 오름차순 정렬 검증"""
        inventory = InventoryPage(driver)
        
        inventory.sort_by('lohi')
        
        prices = inventory.get_all_prices()
        
        assert prices == sorted(prices), f'가격 정렬 실패, 실제 순서: {prices}'
    
    @pytest.mark.P0
    def test_inv_03_add_to_cart(self, driver):
        """INV-03: 장바구니 담기 시 뱃지 카운트 증가"""
        inventory = InventoryPage(driver)
        
        inventory.add_first_item()
        
        count = inventory.get_badge_count()
        assert count == 1, f'장바구니 담기 후 뱃지 숫자가 틀림. 기대: 1, 실제: {count}'
    
    @pytest.mark.P1
    def test_inv_06_cart_retention(self, driver):
        """INV-06: 새로고침 시 장바구니 상태 유지 검증"""
        inventory = InventoryPage(driver)
        inventory.add_first_item()

        driver.refresh()
        
        count = inventory.get_badge_count()
        assert count == 1, '새로고침 후 장바구니가 초기화되었습니다 (세션 유지 실패)'
    

    