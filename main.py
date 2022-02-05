# python配下自動でimport
from selenium import webdriver
from dotenv import load_dotenv
import os


load_dotenv()
WEBDRIVERPATH = os.getenv("WEBDRIVERPATH")
TARGETURL = os.getenv("TARGETURL")


def dev_lambda_handler(event, context):
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
    browser = webdriver.Chrome(
        WEBDRIVERPATH,
        options=options
    )

    browser.get(url)
    title = browser.title
    browser.close()

    return title


if __name__ == "__main__":
    print(dev_lambda_handler("event", "context"))
