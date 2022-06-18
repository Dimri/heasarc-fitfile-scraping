import time
from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import estimate_source_angles_detectors as esad

PATH = '/Downloads/chromedriver' # PATH to ChromeDriver
ser = Service(PATH)
driver = webdriver.Chrome(service=ser)
driver.maximize_window()

df = pd.read_csv('gbmdatacleaned.csv', index_col=0)

# indices of GRBs to download
reqdidx = set()

grbnames = []
ra = []
dec = []
year = []

# populate array with apt info
for i in reqdidx:
    grbnames.append(df.iloc[i]['name'])
    ra.append(df.iloc[i]['ra_val'])
    dec.append(df.iloc[i]['dec_val'])
    year.append(df.iloc[i]['trigger_time'][:4])

# download trigdat_all file    
for i in range(len(ra)):
    ADDRESS = 'https://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/' + year[i] + '/bn' + grbnames[i][3:] + '//current/'
    driver.get(ADDRESS)
    time.sleep(0.5)
    link = driver.find_element(By.PARTIAL_LINK_TEXT, value='glg_trigdat_all_bn' + grbnames[i][3:])
    # download
    link.click()

# download fitfile corresponding to brightest detector    
for i in range(len(ra)):
    ADDRESS = 'https://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/' + year[i] + '/bn' + grbnames[i][3:] + '//current/'
    driver.get(ADDRESS)
    time.sleep(0.5)
    link = driver.find_element(By.PARTIAL_LINK_TEXT, value='glg_trigdat_all_bn' + grbnames[i][3:])
    # brightest detector name
    b = esad.angle_to_grb(ra[i], dec[i], '/Users/dimrisudhanshu/Downloads/' + link.text)
    # download
    driver.find_element(By.PARTIAL_LINK_TEXT, value='glg_tte_' + b[0]).click() 