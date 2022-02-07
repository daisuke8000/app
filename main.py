# python配下自動でimport
from selenium import webdriver
from dotenv import load_dotenv
from time import sleep
import os

load_dotenv()
WEBDRIVERPATH = os.getenv("WEBDRIVERPATH")
TARGETURL = os.getenv("TARGETURL")
LOGINEMAIL = os.getenv("LOGINEMAIL")
LOGINPASSWORD = os.getenv("LOGINPASSWORD")


def lambda_handler(event, context):
    url = TARGETURL

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--hide-scrollbars")
    options.add_argument("--single-process")
    # options.add_argument("--ignore-certificate-errors")
    # options.add_argument("--window-size=880x996")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--homedir=/tmp")
    # options.binary_location = "/opt/python/bin/headless-chromium"

    # ブラウザの定義
    driver = webdriver.Chrome(
        WEBDRIVERPATH,
        options=options
    )

    try:
        driver.get(url)
        print(url)
        sleep(3)
        ## login
        title = input_login(driver)
        sleep(3)
    except:
        driver.close()
    finally:
        driver.close()

    return


def input_login(driver):
    title = driver.title
    driver.find_element_by_class_name('modal-trigger').click()
    input_email = driver.find_element_by_id('your-id')
    input_password = driver.find_element_by_id('your-password')
    input_email.send_keys(LOGINEMAIL)
    input_password.send_keys(LOGINPASSWORD)
    btn_login = driver.find_element_by_id('login-btn')
    btn_login.click()
    get_my_page = driver.find_element_by_id('mypage-member-name')
    print(get_my_page.text)
    # logouton
    driver.find_element_by_class_name('logouton').click()
    return title


if __name__ == "__main__":
    print(lambda_handler("event", "context"))
