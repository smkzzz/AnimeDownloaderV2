import time
import os
import pickle
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils import *
from config import *


class Driver ():
    def __init__(self) -> None:
        create_loading("Initializing browser...", "red", self.driver_start)

    def driver_start(self):
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.get("https://kwik.cx/f/mIqErRexBOS8")
        self.is_cookie_exist(driver)

    def is_cookie_exist(self, driver):
        if(os.path.isfile('kwik.pkl')):
            cookies = pickle.load(open("kwik.pkl", "rb"))
            for cookie in cookies:
                if(cookie['domain'] == 'kwik.cx' and "ppu_exp" in cookie['name'] and self.is_cookie_expired(cookie)):
                    return self.get_new_cookie(driver)
                driver.add_cookie(cookie)
        else:
            pickle.dump(driver.get_cookies(), open("kwik.pkl", "wb"))

    def is_cookie_expired(self, cookie):
        if 'expiry' not in cookie:
            return False
        expiration_time = cookie['expiry']
        current_time = int(time.time())
        return current_time > expiration_time

    def get_new_cookie(self, driver):
        print("Getting new cookie")
        create_msg("In Process", "Obtaining a fresh cookie.",
                   TEXT_MSG_COLOR[0])
        driver.get("https://kwik.cx/f/mIqErRexBOS8")
        pickle.dump(driver.get_cookies(), open("kwik.pkl", "wb"))
