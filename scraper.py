import time

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from utils.estimate_source_angles_detectors import angle_to_grb
from grb import GRB

PATH_TO_CHROME_DRIVER = r"/Downloads/chromedriver"  # Path to ChromeDriver
DOWNLOAD_PATH = r"C:\Users\hhsud\Downloads\GRB"  # Download directory


def initialize():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": DOWNLOAD_PATH}
    chrome_options.add_argument("log-level=3")
    chrome_options.add_experimental_option("prefs", prefs)
    ser = Service(PATH_TO_CHROME_DRIVER)
    driver = webdriver.Chrome(service=ser, options=chrome_options)
    driver.maximize_window()
    return driver


driver = initialize()


def download(link):
    # check if file is present
    path = Path(DOWNLOAD_PATH) / link.text
    if path.exists():
        print(f"{link.text} already downloaded!")
        return

    # download
    link.click()
    # wait for file to downloaded
    while not path.exists():
        time.sleep(0.5)
    print(f"Downloaded : {link.text}")


def get_address(grb):
    return f"https://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/{grb.year}/bn{grb.number}//current/"


def download_trigdat_files(grb):
    # open site
    driver.get(get_address(grb))
    # wait for site loading
    time.sleep(0.5)
    # link contains grb number
    link = driver.find_element(
        By.PARTIAL_LINK_TEXT, value=f"glg_trigdat_all_bn{grb.number}"
    )
    # download the file
    download(link)
    return link.text


def download_fitfile(grb, filename):
    # name of the brightest detector is the first value of the returned tuple
    brightest_detector = angle_to_grb(grb.ra, grb.dec, f"{DOWNLOAD_PATH}/{filename}")

    # download
    link2 = driver.find_element(
        By.PARTIAL_LINK_TEXT, value=f"glg_tte_{brightest_detector[0]}"
    )
    download(link2)


def main():
    # names of GRB files to download
    grb_names = ["GRB120403857", "GRB120227725", "GRB141205018"]
    for name in grb_names:
        grb = GRB(name)
        print(grb)
        # download trigdat_all file and return the filename
        filename = download_trigdat_files(grb)
        # download fitfile corresponding to the brightest detector
        download_fitfile(grb, filename)


if __name__ == "__main__":
    main()
