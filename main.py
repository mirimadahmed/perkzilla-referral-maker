from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


class wait_for_text_to_start_with(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            element_text = EC._find_element(driver, self.locator).get_attribute("value")
            print(element_text)
            return "@" in element_text
        except StaleElementReferenceException:
            return False
        
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("start-maximized")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

mail = "https://temp-mail.org"
refer = "YOUR REFERRAL LINK"

count = 100
while count > 0:
    count = count - 1
    # open mail
    driver = webdriver.Chrome(options=options, executable_path='./chromedriver')

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                                        'Chrome/85.0.4183.102 Safari/537.36'})

    driver.get(mail)
    # wait for mail to appear
    WebDriverWait(driver, 20).until(wait_for_text_to_start_with((By.ID, 'mail')))
    span_element = driver.find_element_by_css_selector("#mail")

    # open
    mymail = span_element.get_attribute("value")
    print(mymail)

    driver.execute_script("window.open('');")
    # Switch to the new window
    driver.switch_to.window(driver.window_handles[1])
    driver.get(refer)
    time.sleep(3)
    driver.find_element_by_css_selector('#pkemail').send_keys(mymail);
    driver.find_element_by_css_selector('#pksubmit').click()



    driver.switch_to.window(driver.window_handles[0])
    wait = WebDriverWait(driver, 10)
    elems = driver.find_elements_by_css_selector('div.inbox-dataList > ul > li')
    time.sleep(3)
    while len(elems) < 2:
        time.sleep(3)
        elems = driver.find_elements_by_css_selector('div.inbox-dataList > ul > li')
    
    elems[1].click()
    time.sleep(10)
    confirm = driver.find_elements_by_xpath("//*[contains(text(), 'Confirm Your Email')]")
    link = confirm[0].get_attribute("href")
    # open this link in new tab
    driver.execute_script("window.open('');")
    # Switch to the new window
    driver.switch_to.window(driver.window_handles[2])
    driver.get(link)
    time.sleep(10)
    driver.quit()
