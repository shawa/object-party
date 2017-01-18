from typing import Dict, Union
from selenium import webdriver
import os
from datetime import datetime

TS_FMT = '%Y-%m-%d-%H-%M-%S'  # type: str
TIMESTAMP = datetime.now().strftime(TS_FMT)  # type: str
LOG_DIR = os.path.abspath('har') + '/' + TIMESTAMP  # type: str

ABOUT_CONFIG = {
    'devtools.netmonitor.har.enableAutoExportToFile': True,
    'devtools.netmonitor.har.defaultLogDir': LOG_DIR,
    'devtools.netmonitor.har.defaultFileName': TS_FMT
}  # type: Dict[str, Union[bool, str]]


def get_driver(config: Dict[str, Union[bool, str]]) -> webdriver.firefox.webdriver.WebDriver:
    profile = webdriver.FirefoxProfile()
    for k, v in config.items():
        profile.set_preference(k, v)

    driver = webdriver.Firefox(profile)
    return driver

driver = get_driver(ABOUT_CONFIG)
driver.get("https://lobster.guitars")

input("waiting")

driver.close()
