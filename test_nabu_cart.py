import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture 
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def handle_password(driver, wait, password):
    try:
        password_link = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "password-link")))
        password_link.click()
        password_field = wait.until(EC.presence_of_element_located((By.ID, "Password")))
        password_field.send_keys(password)
        password_field.send_keys(Keys.ENTER)
    except:
        pass

def search_for_product(driver, wait, product_name):
    search_trigger = wait.until(EC.element_to_be_clickable((By.XPATH, "//summary[@aria-label='Search']")))
    search_trigger.click()
    search_input = wait.until(EC.presence_of_element_located((By.ID, "Search-In-Modal")))
    search_input.send_keys(product_name)
    search_input.send_keys(Keys.ENTER)

def add_product_to_cart(driver, wait):
    first_product = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".grid__item")))
    first_product.click()
    add_to_cart_btn = wait.until(EC.element_to_be_clickable((By.NAME, "add")))
    add_to_cart_btn.click()

def test_search_and_add_to_cart(driver):
    wait = WebDriverWait(driver, 15)
    
    driver.get("https://nabu-test-store.myshopify.com/")

    handle_password(driver, wait, "AdNabuQA")

    search_for_product(driver, wait, "ball")

    add_product_to_cart(driver, wait)

    success_msg = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cart-notification__heading")))
    assert "Item added to your cart" in success_msg.text
    print("\nSuccess: Product added to cart successfully!")