import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import pickle
import argparse

def sessionCreator(username, password):
    username = username
    password = password

    login_url = "https://www.pinterest.com/login/"
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    driver = uc.Chrome(options=options)

    driver.get(login_url)

    driver.find_element(By.NAME, "id").send_keys(username)

    driver.find_element(By.NAME, "password").send_keys(password)

    driver.find_element(By.XPATH,
                        "//*[@id=\"mweb-unauth-container\"]/div/div[3]/div/div/div[3]/form/div[7]/button").click()

    time.sleep(10)

    cookies = driver.get_cookies()

    driver.quit()

    with open("pinterest_cookies.pkl", "wb") as f:
        pickle.dump(cookies, f)
    print("Cookies saved as pinterest_cookies.pkl")


parser = argparse.ArgumentParser(description="Pinterestten reels oluşturma scripti")
parser.add_argument("-u", "--username", help="Pinterest isminiz", required=True)
parser.add_argument("-p", "--password", help="Pinterest şifreniz", required=True)
args = parser.parse_args()

sessionCreator(args.username, args.password)