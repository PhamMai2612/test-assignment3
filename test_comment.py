from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Utils.CookieLoader import CookieLoader

TINHTE = "https://tinhte.vn"
TINHTE_COMMENT_POST = "https://tinhte.vn/thread/review-mazda-cx5-2017.3293178/"
COMMENT = "mazda đồ"
COMMENT_BOX_XPATH = '//textarea[@class="post-reply-input"]'
POST_BUTTON_XPATH = '//button[@class="jsx-3593820457 post-reply-submit active"]'
COMMENT_POSTED_BOX = '//div[@data-author="nguyen_thi_dau"]/span'
DELAY = 10


def test_write_comment_basic_flow():
  """
  WC1: Basic flow of user comment procedure
  :return: assert Passed if user commented successfully
  """
  driver = CookieLoader.load_cookie()
  driver.get(TINHTE_COMMENT_POST)

  try:
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, COMMENT_BOX_XPATH))).send_keys(COMMENT)

    WebDriverWait(driver, DELAY)\
      .until(EC.presence_of_element_located((By.XPATH, POST_BUTTON_XPATH))).click()

    commented_text = WebDriverWait(driver, DELAY) \
      .until(EC.presence_of_element_located((By.XPATH, COMMENT_POSTED_BOX))).text

    assert COMMENT == commented_text
  except TimeoutException:
    raise TimeoutException("Time out when in test_write_comment_basic_flow")


def test_write_comment_sicker():
  """
  WC2: Alternative flow of comment with sticker
  :return: assert Passed if user commented successfully
  """
  driver = CookieLoader.load_cookie()
  driver.get(TINHTE_COMMENT_POST)

  try:
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, COMMENT_BOX_XPATH))).send_keys(COMMENT)

    sicker_path = '//button[@title="Stickers"]'
    imoji_xpath= '//div[@class="jsx-3529665607 sticker-list"]//button[2]'

    driver.find_element_by_xpath(sicker_path).click()

    WebDriverWait(driver, DELAY) \
      .until(EC.presence_of_element_located((By.XPATH, imoji_xpath))).click()

    WebDriverWait(driver, DELAY) \
      .until(EC.presence_of_element_located((By.XPATH, POST_BUTTON_XPATH))).click()

    commented_text = WebDriverWait(driver, DELAY) \
      .until(EC.presence_of_element_located((By.XPATH, COMMENT_POSTED_BOX))).text

    assert COMMENT == commented_text
  except TimeoutException:
    raise TimeoutException("Time out when in test_write_comment_sicker")


def test_write_space_comment():
  """
  WC3: Exceptional flow of user comment procedure
  :return: assert Passed if having warning text when user comment space
  """
  driver = CookieLoader.load_cookie()
  driver.get(TINHTE_COMMENT_POST)

  try:
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, COMMENT_BOX_XPATH))).send_keys("      ")

    WebDriverWait(driver, DELAY) \
      .until(EC.presence_of_element_located((By.XPATH, POST_BUTTON_XPATH))).click()

    error_xpath = '//p[@class="jsx-3593820457 error"]'
    error_text = WebDriverWait(driver, DELAY) \
      .until(EC.presence_of_element_located((By.XPATH, error_xpath))).text

    define_error_text = "Vui lòng không để trống bình luận"
    assert define_error_text == error_text

  except TimeoutException:
    raise TimeoutException("Time out when in test_write_space_comment")


def test_write_comment_and_edit():
  """
  WC4: Alternative flow when editing a comment
  :return: assert Passed if user commented successfully
  """
  driver = CookieLoader.load_cookie()
  driver.get(TINHTE_COMMENT_POST)

  try:
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, COMMENT_BOX_XPATH))).send_keys(COMMENT)

    WebDriverWait(driver, DELAY) \
      .until(EC.presence_of_element_located((By.XPATH, POST_BUTTON_XPATH))).click()

    commented_text = WebDriverWait(driver, DELAY) \
      .until(EC.presence_of_element_located((By.XPATH, COMMENT_POSTED_BOX))).text

    assert COMMENT == commented_text

    edit_xpath = '//button[@class="jsx-2274533257 thread-action"]'
    driver.find_element_by_xpath(edit_xpath).click()

    edit_text_path = '//div[@id="post-reply-"]//textarea[@class="post-reply-input"]'
    WebDriverWait(driver, 2)\
      .until(EC.presence_of_element_located((By.XPATH, edit_text_path)))\
      .send_keys("edit")

    WebDriverWait(driver, DELAY) \
      .until(EC.presence_of_element_located((By.XPATH, POST_BUTTON_XPATH))).click()

    edit_commented_text = WebDriverWait(driver, DELAY) \
      .until(EC.presence_of_element_located((By.XPATH, COMMENT_POSTED_BOX))).text

    assert "edit" in edit_commented_text
  except TimeoutException:
    raise TimeoutException("Time out when in test_write_comment_and_edit")


def test_write_comment_and_delete():
  """
  WC5: Exception flow when delete a comment
  :return: assert Passed if user commented deleted successfully
  """
  driver = CookieLoader.load_cookie()
  driver.get(TINHTE_COMMENT_POST)

  try:
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, COMMENT_BOX_XPATH))).send_keys(COMMENT)

    WebDriverWait(driver, DELAY) \
      .until(EC.presence_of_element_located((By.XPATH, POST_BUTTON_XPATH))).click()

    commented_text = WebDriverWait(driver, DELAY) \
      .until(EC.presence_of_element_located((By.XPATH, COMMENT_POSTED_BOX))).text

    assert COMMENT == commented_text

    delete_xpath = '//div[@class="jsx-2274533257 thread-comment__action--right"]//button[2]'
    comfirm_delete_path = "//button[@class='jsx-3932553558 button active']"

    WebDriverWait(driver, DELAY) \
      .until(EC.presence_of_element_located((By.XPATH, delete_xpath))).click()

    driver.find_element_by_xpath(comfirm_delete_path).click()

    commented_text = WebDriverWait(driver, DELAY) \
      .until(EC.presence_of_element_located((By.XPATH, COMMENT_POSTED_BOX))).text

    assert COMMENT != commented_text
  except TimeoutException:
    raise TimeoutException("Time out when in test_write_comment_and_delete")