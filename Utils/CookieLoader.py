import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class CookieLoader:

  """
    This class aims for get cookies after logging in
    Later when running the test, saved cookies is used to run test
  """

  COOKIE_PATH = 'cookies.json'

  @staticmethod
  def get_cookie():
    TINH_TE = 'https://tinhte.vn/login/'
    USERNAME = "nguyen_thi_dau"
    PASS = "Hung8787"
    USERNAME_XPATH = '//input[@id="ctrl_pageLogin_login" and @class="textCtrl"]'
    PASSWORD_XPATH = '//input[@id="ctrl_pageLogin_password" and @class="textCtrl"]'
    BUTTON_XPATH = '//*[@id="pageLogin"]/dl[3]/dd/input'
    DELAY = 3

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(TINH_TE)

    WebDriverWait(driver, DELAY) \
      .until(EC.presence_of_element_located((By.XPATH, USERNAME_XPATH))) \
      .send_keys(USERNAME)

    WebDriverWait(driver, DELAY) \
      .until(EC.element_to_be_clickable((By.XPATH, PASSWORD_XPATH))) \
      .send_keys(PASS)

    driver.find_element_by_xpath(BUTTON_XPATH).click()


    with open(CookieLoader.COOKIE_PATH, 'w') as file:
      json.dump(driver.get_cookies(), file)

    driver.close()

  @staticmethod
  def load_cookie():
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--no-default-browser-check')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-default-apps')
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("https://tinhte.vn/")
    driver.delete_all_cookies()

    with open(CookieLoader.COOKIE_PATH, 'r') as cookiesfile:
      cookies = json.load(cookiesfile)
    for cookie in cookies:
      driver.add_cookie(cookie)

    return driver