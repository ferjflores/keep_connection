#!/usr/bin/python3

import sys
import getopt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException

DEFAULT_ROUTER_URL = "http://192.168.88.1"
DEFAULT_ADMIN_PW = "admin"
DEFAULT_HELP_MESSAGE = 'reset.py -u <router_url> -o <admin_password>'
DEFAULT_PARAM_MESSAGE = 'If yo want to specify these values please use: \n {}'.format(DEFAULT_HELP_MESSAGE)


def main(argv):
    url = DEFAULT_ROUTER_URL
    password = DEFAULT_ADMIN_PW

    try:
        opts, args = getopt.getopt(argv, "hu:p:", ["url=", "password="])
        for opt, arg in opts:
            if opt == '-h':
                print(DEFAULT_HELP_MESSAGE)
                sys.exit()
            elif opt in ("-u", "--url"):
                url = arg
            elif opt in ("-p", "--password"):
                password = arg
    except getopt.GetoptError:
        print('reset.py -u <router_url> -o <admin_password>')

    if url == DEFAULT_ROUTER_URL and password == DEFAULT_ADMIN_PW:
        print('Using default url ("http://192.168.88.1") and default password ("admin")\n {}'
              .format(DEFAULT_PARAM_MESSAGE))
    else:
        if url == DEFAULT_ROUTER_URL:
            print('Using default url ("http://192.168.88.1") \n{}'.format(DEFAULT_PARAM_MESSAGE))
        if password == DEFAULT_ADMIN_PW:
            print('Using default password ("admin")\n {}'.format(DEFAULT_PARAM_MESSAGE))

    reset(url, password)


def reset(url, pw):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('no-sandbox')

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    try:
        assert "3G" in driver.title
    except AssertionError:
        print("Error connecting to {}".format(url))

    password = driver.find_element_by_id("password")
    password.send_keys(pw, Keys.ENTER)
    wait = WebDriverWait(driver, 3)

    try:
        wait.until(EC.alert_is_present())

        alert = driver.switch_to.alert
        alert.accept()
        print('Incorrect Password')
    except TimeoutException as error:
        pass
    print('password accepted')

    driver.switch_to.frame('listfrm')
    selector_advanced_configuration = "labContent4"
    # wait.until(EC.visibility_of_element_located(By.ID(selector_advanced_configuration)))
    advanced_configuration = driver.find_element_by_id(selector_advanced_configuration)
    advanced_configuration.click()

    driver.switch_to.default_content()
    driver.switch_to.frame('basefrm')
    system = driver.find_element_by_id('labContent2')
    system.click()

    reboot = driver.find_element_by_id('labContent4')
    reboot.click()

    reboot_confirm = driver.find_element_by_id('labControl2')
    reboot_confirm.click()
    Alert(driver).accept()
    print("Reboot successful")

    driver.close()


if __name__ == "__main__":
    main(sys.argv[1:])
