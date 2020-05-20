import socket
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException


def reset(url, pw):
    message = ''
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('no-sandbox')

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    try:
        assert "3G" in driver.title
    except AssertionError:
        return "Error connecting to {}".format(url)

    password = driver.find_element_by_id("password")
    password.send_keys(pw, Keys.ENTER)
    wait = WebDriverWait(driver, 3)

    try:
        wait.until(EC.alert_is_present())

        alert = driver.switch_to.alert
        alert.accept()
        message += 'Incorrect Password'
        return message
    except TimeoutException as error:
        message += 'password accepted\n'

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
    message = "\nReboot successful"
    driver.close()
    return message


def check_dns_resolution(hostname):
    message = 'DNS resolution working'
    try:
        socket.gethostbyname(hostname)
        return True, message
    except Exception as error:
        message = error
    return False, message


def is_connected(host):
    try:
        s = socket.create_connection((host, 80), 2)
        s.close()
        message = 'Connected to host {} port {}'.format(host, 80)
        return True, message
    except Exception as error:
        message = error
    return False, message
