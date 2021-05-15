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


def test_create_post_basic_flow():
  """
  CP1: Basic flow of writing post
  """
  post_content = "iphone 12 mau tim"
  driver = CookieLoader.load_cookie()
  driver.get(TINHTE)

  try:
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, BUTTON_CREATE_POST))).click()

    WebDriverWait(driver, DELAY) \
      .until(EC.presence_of_element_located((By.XPATH, POST_BOX_XPATH)))\
      .send_keys(post_content)

    sleep(2)
    driver.find_element_by_xpath(POST_BUTTON_XPATH).click()

    commented_text = WebDriverWait(driver, DELAY) \
      .until(EC.presence_of_element_located((By.XPATH, POSTED_BOX_XPATH))).text

    assert post_content == commented_text
  except TimeoutException:
    raise TimeoutException("Time out when in test_create_post_basic_flow")


def test_create_post_less_or_equal_ten_words():
  """
  CP2: Exception flow of a post has less than or equal 10 words required
  """
  post_content = "ip 12 timm" # 10 characters
  warning_message_xpath = '//span[@class="jsx-1783754700 text"]'
  warning_mess = "Bạn phải gõ dài hơn 10 kí tự mới được nhé :D"
  driver = CookieLoader.load_cookie()
  driver.get(TINHTE)

  try:
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, BUTTON_CREATE_POST))).click()

    WebDriverWait(driver, DELAY) \
      .until(EC.presence_of_element_located((By.XPATH, POST_BOX_XPATH))) \
      .send_keys(post_content)

    warning_text = WebDriverWait(driver, DELAY) \
      .until(EC.presence_of_element_located((By.XPATH, warning_message_xpath))).text

    assert warning_mess == warning_text
  except TimeoutException:
    raise TimeoutException("Time out when in test_create_post_less_or_equal_ten_words")


def test_create_post_with_background():
  """
  CP3: Alternative flow of post with selective background
  """
  post_content = "iphone 12 mau tim"
  driver = CookieLoader.load_cookie()
  driver.get(TINHTE)
  background_list_xpath = "//button[@class='jsx-1783754700 thread-background-switch']"
  theme_chosen_xpath = "//div[@class='jsx-1783754700 thread-background-container visible']/img[1]"

  try:
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, BUTTON_CREATE_POST))).click()

    WebDriverWait(driver, DELAY) \
      .until(EC.presence_of_element_located((By.XPATH, POST_BOX_XPATH))) \
      .send_keys(post_content)

    driver.find_element_by_xpath(background_list_xpath).click()

    WebDriverWait(driver, DELAY) \
      .until(EC.element_to_be_clickable((By.XPATH, theme_chosen_xpath))).click()

    sleep(2)
    driver.find_element_by_xpath(POST_BUTTON_XPATH).click()

    commented_text = WebDriverWait(driver, DELAY) \
      .until(EC.presence_of_element_located((By.XPATH, POSTED_BOX_XPATH))).text

    assert post_content == commented_text
  except TimeoutException:
    raise TimeoutException("Time out when in test_create_post_with_background")


def test_create_post_and_cancel():
  """
  CP1: Basic flow of writing post
  """
  post_content = "iphone 12 mau tim"
  driver = CookieLoader.load_cookie()
  driver.get(TINHTE)
  cancel_button = '//div[@role="dialog"]//div[@class="jsx-1783754700 top-area"]//button'

  try:
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, BUTTON_CREATE_POST))).click()

    WebDriverWait(driver, DELAY) \
      .until(EC.presence_of_element_located((By.XPATH, POST_BOX_XPATH))) \
      .send_keys(post_content)

    driver.find_element_by_xpath(cancel_button).click()

    boxes = driver.find_elements_by_xpath(POST_BOX_XPATH)

    assert len(boxes) == 0
  except TimeoutException:
    raise TimeoutException("Time out when in test_create_post_basic_flow")
