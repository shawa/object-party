from typing import Dict, Union, List

import time
import os
import logging

import clize

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from datetime import datetime

TS_FMT = '%Y-%m-%d-%H-%M-%S'  # type: str
TIMESTAMP = datetime.now().strftime(TS_FMT)  # type: str
LOG_DIR = os.path.abspath('har') + '/' + TIMESTAMP  # type: str
EXT_DIR = os.path.abspath('ff_addons')  # type: str

EXTENSIONS = [EXT_DIR + '/' + filename
              for filename in os.listdir(EXT_DIR)]  # type: List[str]

ABOUT_CONFIG = {
    'devtools.netmonitor.har.enableAutoExportToFile': True,
    'devtools.netmonitor.har.defaultLogDir': LOG_DIR,
    'devtools.netmonitor.har.defaultFileName': TS_FMT,
    'extensions.netmonitor.har.autoConnect': True,
}  # type: Dict[str, Union[bool, str]]

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


def get_driver(config: Dict[str, Union[bool, str]],
               extensions: List[str]) -> webdriver.firefox.webdriver.WebDriver:
    profile = webdriver.FirefoxProfile()
    logger.info('Created new Firefox Profile')

    for extension in extensions:
        profile.add_extension(extension)
        logger.info("Added extension {}".format(extension))

    for k, v in config.items():
        profile.set_preference(k, v)
        logger.info('Set `{}` to `{}`'.format(k, v))

    driver = webdriver.Firefox(profile)
    logger.info('Launched new Firefox driver with custom profile')

    return driver


def crawl(driver, urls):
    def toggle_network_panel(driver, delay=1):
        driver.find_element_by_tag_name('body').send_keys(Keys.META + Keys.ALT + 'q')
        time.sleep(delay)

    failures = []
    # initial setup, we need the network panel open
    for url in urls:
        logger.info("Fetching {}".format(url))
        try:
            driver.get(url)
        except Exception as e:
            logger.error(e)
            logger.error("Failed to fetch {}, exception below".format(url))
            failures.append(url)
            continue
        logger.info("Fetched  {}".format(url))
        toggle_network_panel(driver)
        logger.info("Opened dev tools")
        driver.refresh()
        logger.info("Refreshed")
        time.sleep(15)
        logger.info("Closing dev tools")
        toggle_network_panel(driver, delay=0.5)

    logger.info("Completed")
    if failures:
        logger.warn("Failures: {}".format(failures))


def tourls(domains, protocol='http'):
    rows = (l.split(',') for l in domains)
    for number, domain in rows:
        yield protocol + '://' + domain


def main(domainsfile, *, logdir='har'):
    logger.info('Launched crawler')

    driver = get_driver(ABOUT_CONFIG, EXTENSIONS)
    try:
        with open(domainsfile, 'r') as domains:
            crawl_targets = (u for u in domains if not u.startswith('#'))
            urls = tourls(crawl_targets)
            crawl(driver, urls)
    except KeyboardInterrupt:
        logger.info('Killed, closing driver')

    driver.quit()


if __name__ == '__main__':
    clize.run(main)
