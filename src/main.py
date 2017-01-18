from typing import Dict, Union, List

import time
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime

Driver = webdriver.firefox.webdriver.WebDriver

TS_FMT = '%Y-%m-%d-%H-%M-%S'  # type: str
TIMESTAMP = datetime.now().strftime(TS_FMT)  # type: str
LOG_DIR = os.path.abspath('har') + '/' + TIMESTAMP  # type: str
EXT_DIR = os.path.abspath('ff_addons') # type: str

EXTENSIONS = [EXT_DIR + '/' + filename
              for filename in os.listdir(EXT_DIR)]  # type: List[str]

ABOUT_CONFIG = {
    'devtools.netmonitor.har.enableAutoExportToFile': True,
    'devtools.netmonitor.har.defaultLogDir': LOG_DIR,
    'devtools.netmonitor.har.defaultFileName': TS_FMT,
    'extensions.netmonitor.har.autoConnect': True,
}  # type: Dict[str, Union[bool, str]]


def get_driver(config: Dict[str, Union[bool, str]],
               extensions: List[str]) -> webdriver.firefox.webdriver.WebDriver:
    profile = webdriver.FirefoxProfile()

    for extension in extensions:
        profile.add_extension(extension)

    for k, v in config.items():
        profile.set_preference(k, v)

    driver = webdriver.Firefox(profile)

    return driver


def crawl(driver, urls):
    def toggle_network_panel(driver):
        driver.find_element_by_tag_name('body').send_keys(Keys.META + Keys.ALT + 'q')
        time.sleep(2)

    # initial setup, we need the network panel open
    for url in urls:
        driver.get(url)
        toggle_network_panel(driver)
        driver.refresh()
        time.sleep(10)
        toggle_network_panel(driver)


def main():
    driver = get_driver(ABOUT_CONFIG, EXTENSIONS)

    urls = [
        "https://apple.com",
        "https://gmail.com",
        "https://reddit.com",
    ]

    crawl(driver, urls)
    driver.close()


if __name__ == '__main__':
    main()
