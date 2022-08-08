# #!/usr/bin/env python
from xml.etree.ElementTree import tostring
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By

print ('Starting the browser...')    
options = ChromeOptions()

# uncomment to run on the CI/CD pipeline
options.add_argument("--headless")

# uncomment to debug locally
# options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)

# Start the browser and login with standard_user
def login (user, password):
    print ('# ---')
    print ('# Login')
    driver.get('https://www.saucedemo.com/')

    print (f'typing username "{user}"...')
    driver.find_element(By.CSS_SELECTOR, '#user-name').send_keys(user)

    print (f'typing password "{password}"...')
    driver.find_element(By.CSS_SELECTOR, '#password').send_keys(password)

    print (f'clicking login button...')
    driver.find_element(By.CSS_SELECTOR, '#login-button').click()

    print (f'checking the inventory list is displayed after login...')
    assert driver.find_element(By.CSS_SELECTOR, '#inventory_container').is_displayed

    print (f'login completed successfully')

def add_products_to_cart ():
    print ('# ---')
    print ('# Add products to cart')

    print ('finding all Add Product buttons...')
    add_buttons = driver.find_elements(By.CSS_SELECTOR, '.btn_inventory')
    
    buttons_count = len(add_buttons)
    print (f'{buttons_count} buttons found')

    for add_button in add_buttons:
        print(f'adding product {add_button.get_attribute("id")}...')
        add_button.click()

    print (f'checking the cart has {buttons_count} items')
    shopping_cart_badge = driver.find_element(By.CSS_SELECTOR, '.shopping_cart_badge').text
    assert int(shopping_cart_badge) == int(buttons_count)

    print ('products added successfully')

def remove_products_from_cart ():
    print ('# ---')
    print ('# Remove products from cart')

    print ('clicking the shopping cart link...')
    driver.find_element(By.CSS_SELECTOR, '.shopping_cart_link').click()

    print ('finding all Remove buttons...')
    remove_buttons = driver.find_elements(By.CSS_SELECTOR, '.cart_button')
    
    buttons_count = len(remove_buttons)
    print (f'{buttons_count} buttons found')

    for remove_button in remove_buttons:
        print(f'removing product {remove_button.get_attribute("id")}...')
        remove_button.click()

    print (f'checking the cart has 0 items')
    assert len(driver.find_elements(By.CSS_SELECTOR, '.shopping_cart_badge')) == 0
    assert len(driver.find_elements(By.CSS_SELECTOR, '.cart_button')) == 0

    print ('products removed successfully')

login('standard_user', 'secret_sauce')
add_products_to_cart()
remove_products_from_cart()
