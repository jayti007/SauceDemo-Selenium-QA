import pytest
from pages.login_page import LoginPage

@pytest.mark.usefixtures('driver')
class TestLogin:
    """로그인(Auth) 기능 관련 테스트 시니리오"""

    @pytest.mark.P0
    def test_auth_01_valid_login(self, driver):
        """AUTH-01: 정상 로그인 및 세션 쿠키 확인"""
        login_page = LoginPage(driver)
        driver.get('https://www.saucedemo.com/')

        login_page.login('standard_user', 'secret_sauce')

        assert 'inventory.html' in driver.current_url, '로그인 후 페이지 이동 실패'

    @pytest.mark.P0
    def test_auth_02_locked_user(self, driver):
        """AUTH-02: 잠긴 계정 로그인 시 에러 메시지 검증"""
        login_page = LoginPage(driver)
        driver.get('https://www.saucedemo.com/')
        
        login_page.login('locked_out_user', 'secret_sauce')

        error_text = login_page.get_error_message()
        assert 'locked out' in error_text, '잠긴 계정 에러 메시지가 올바르지 않음   '
    
    @pytest.mark.P1
    def test_auth_03_empty_fields(self, driver):
        """AUTH-03: 아이디/비번 공란 시 유효성 검증"""
        login = LoginPage(driver)
        driver.get('https://www.saucedemo.com/')

        login.login('', '')
        
        assert 'Username is required' in login.get_error_message(), '아이디/비번 공란 시 뜨는 에러 메시지가 올바르지 않음'
    
    @pytest.mark.P1
    def test_auth_05_direct_access(self, driver):
        """AUTH-05: 로그인 없이 내부 페이지 접근 시 차단 검증"""
        from selenium.webdriver.support.ui import WebDriverWait
        
        driver.get('https://www.saucedemo.com/inventory.html')
        
        # 리디렉션 대기 (최대 5초)
        WebDriverWait(driver, 5).until(
            lambda d: 'inventory.html' not in d.current_url
        )

        assert 'inventory.html' not in driver.current_url, '로그인 없이 내부 페이지로 접근 허용 됨'
        
        login = LoginPage(driver)
        assert 'You can only access' in login.get_error_message()