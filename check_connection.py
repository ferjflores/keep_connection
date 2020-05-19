#!/usr/bin/python3

import socket
import logging
import sys
import getopt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException

REMOTE_SERVER_NAME = "one.one.one.one"
REMOTE_SERVER_IP = "1.1.1.1"
REMOTE_SERVER_ISP = "200.44.32.12"
logging.basicConfig(filename='/tmp/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
DEFAULT_ROUTER_URL = "http://192.168.88.1"
DEFAULT_ADMIN_PW = "admin"
DEFAULT_HELP_MESSAGE = 'check_connection.py -u <router_url> -o <admin_password> -r'
DEFAULT_PARAM_MESSAGE = 'If yo want to specify these values please use: \n {}'.format(DEFAULT_HELP_MESSAGE)


def main(argv):
    url = DEFAULT_ROUTER_URL
    password = DEFAULT_ADMIN_PW
    restart = False

    try:
        opts, args = getopt.getopt(argv, "hu:p:r:", ["url=", "password=", "restart="])
        for opt, arg in opts:
            if opt == '-h':
                print(DEFAULT_HELP_MESSAGE)
                sys.exit()
            elif opt in ("-u", "--url"):
                url = arg
            elif opt in ("-p", "--password"):
                password = arg
            elif opt in ("-r", "--restart"):
                restart = False

    except getopt.GetoptError:
        print(DEFAULT_HELP_MESSAGE)

    if url == DEFAULT_ROUTER_URL and password == DEFAULT_ADMIN_PW:
        print('Using default url ("{}") and default password ("admin")\n {}'
              .format(DEFAULT_ROUTER_URL, DEFAULT_PARAM_MESSAGE))
    else:
        if url == DEFAULT_ROUTER_URL:
            print('Using default url ("{}") \n{}'.format(DEFAULT_ROUTER_URL, DEFAULT_PARAM_MESSAGE))
        if password == DEFAULT_ADMIN_PW:
            print('Using default password ("admin")\n {}'.format(DEFAULT_PARAM_MESSAGE))

    check_dns = check_dns_resolution(REMOTE_SERVER_NAME)
    check_connection = is_connected(REMOTE_SERVER_IP)

    if not check_connection and restart:
        print("reset connection")
        reset(url, password)
    else:
        print("Connection working")


def check_dns_resolution(hostname):
    try:
        socket.gethostbyname(hostname)
        return True
    except Exception as error:
        print(error)
    return False


def is_connected(host):
    try:
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except Exception as error:
        print(error)
    return False


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
