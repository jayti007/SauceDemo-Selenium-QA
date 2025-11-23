import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

@pytest.mark.usefixtures('driver')
class TestCheckout:
    """결제(Checkout) 기능 관련 테스트 시나리오"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """
        [전제조건]
        모든 결제 테스트는 '로그인 -> 상품 담기 -> 장바구니 이동 -> Checkout 클릭'
        상태에서 시작해야 함. 그래서 이걸 미리 다 해둔거!
        """

        driver.get('https://www.saucedemo.com')
        LoginPage(driver).login('standard_user', 'secret_sauce')
        
        inv = InventoryPage(driver)
        inv.add_first_item()
        inv.go_to_cart()
        
        CartPage(driver).click_checkout()

    @pytest.mark.P0
    def test_chk_01_calculate_total(self, driver):
        """CHK-01: 최종 결제 금액 계산 검증 (Item + Tax = Total)"""
        checkout = CheckoutPage(driver)

        checkout.fill_info('Minjae', 'Kim', '12345') # 정보 입력
        
        item_price, tax, total = checkout.get_prices() # 금액 가져오기
        
        expected_total = round(item_price + tax, 2) # 검증: 물건값 + 세금 = 총액
        
        assert total == expected_total, f'계산 오류 발생! 화면 총액: {total}, 예상 총액: {expected_total}'
        
    @pytest.mark.P1
    def test_chk_02_validation(self, driver):
        """CHK-02: 필수 정도(이름) 미입력 시 에러 검증"""
        checkout = CheckoutPage(driver)
        checkout.fill_info('', 'Kim', '12345')

        error = checkout.get_error_message()

        assert 'First Name is required' in error, f'에러 메시지가 틀림. 실제 메시지: {error}'
    
    @pytest.mark.P0
    @pytest.mark.E2E
    def test_chk_04_e2e_flow(self, driver):
        checkout = CheckoutPage(driver)
        checkout.fill_info('Minjae', 'Kim', '12345')
        
        checkout.finish_order()

        msg = checkout.get_complete_message()
        assert 'Thank you' in msg, '결제 완료 페이지가 뜨지 않았음: {msg}'