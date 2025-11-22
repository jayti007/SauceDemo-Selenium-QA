import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope='function')
def driver():
    """각 테스트마다 새로운 WebDriver 인스턴스 생성"""
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized') # 창 최대화
    # options.add_argument("--headless") # CI 환경에서는 주석 해제

    prefs = {
        'credentials_enable_service': False,
        'profile.password_manager_enabled': False
    }
    options.add_experimental_option('prefs', prefs)
    
    options.add_experimental_option('excludeSwitches', ['enabled-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(3)

    yield driver

    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """테스트 실패 시 스크린샷 자동 저장"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == 'call' and rep.failed:
        driver = item.funcargs.get('driver')
        if driver:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            test_name = item.name
            filepath = f'screenshots/{test_name}_{timestamp}.png'

            try:
                driver.save_screenshot(filepath)
                print(f'\n[스크린샷 저장] {filepath}')
            except Exception as e:
                print(f'\n [스크린샷 저장 실패] {e}')