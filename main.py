from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
import time
import pickle

console = Console()


def is_cookie_expired(cookie):
    if 'expiry' not in cookie:
        return False
    expiration_time = cookie['expiry']
    current_time = int(time.time())
    return current_time > expiration_time


def get_new_cookie(driver):
    driver.get("https://kwik.cx/f/mIqErRexBOS8")
    pickle.dump(driver.get_cookies(), open("kwik.pkl", "wb"))


def driverStarter():
    with console.status("[bold red]Initializing webdriver...") as status:
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.get("https://kwik.cx/f/mIqErRexBOS8")
        if(os.path.isfile('kwik.pkl')):
            cookies = pickle.load(open("kwik.pkl", "rb"))
            for cookie in cookies:
                if(cookie['domain'] == 'kwik.cx' and is_cookie_expired(cookie)):
                    print("Session has expired")
                    return get_new_cookie(driver)
                driver.add_cookie(cookie)
        else:
            pickle.dump(driver.get_cookies(), open("kwik.pkl", "wb"))


if __name__ == '__main__':
    os.system("cls")
    driverStarter()
    # anime(driver)
