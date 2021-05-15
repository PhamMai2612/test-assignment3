from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Utils.CookieLoader import CookieLoader

TINHTE = "https://tinhte.vn"
BUTTON_CREATE_POST = "//button[@class='jsx-1783754700 blue-switch ']"
POST_BOX_XPATH = '//textarea[@class="thread-editor-textarea "]'
POST_BUTTON_XPATH = '//div[@role="dialog"]//div[@class="jsx-1783754700 bottom-area"]//button'
POSTED_BOX_XPATH = "//div[@class='jsx-1378818985 thread-title']"
DELAY = 10

post_content = "iphone 12 mau tim"
driver = CookieLoader.load_cookie()
driver.get(TINHTE)

WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, BUTTON_CREATE_POST))).click()

WebDriverWait(driver, DELAY) \
  .until(EC.presence_of_element_located((By.XPATH, POST_BOX_XPATH))) \
  .send_keys(post_content)

sleep(5)
driver.find_element_by_xpath(POST_BUTTON_XPATH).click()

commented_text = WebDriverWait(driver, DELAY) \
  .until(EC.presence_of_element_located((By.XPATH, POSTED_BOX_XPATH))).text

print(commented_text)
