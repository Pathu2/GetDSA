import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

s = Service('chromedriver.exe')

driver = webdriver.Chrome(service=s)
#classes of the elements to be scrapped
heading_class = ".mr-2.text-label-1"
body_class = ".px-5.pt-4"
index = 1
#Created Qdata folder
QDATA_FOLDER = "Qdata"

# Function to return the array of links
def get_links():
    arr = []  
    with open("lc.txt", "r") as file:
        #read line by line
        for line in file:
            arr.append(line)
    return arr


def add_heading(text):
    index_file_path = os.path.join(QDATA_FOLDER, "index.txt")
    with open(index_file_path, "a") as index_file:
        index_file.write(text + "\n")
#store the heading in index.txt file 

def add_link(text):
    index_file_path = os.path.join(QDATA_FOLDER, "Qindex.txt")
    with open(index_file_path, "a", encoding="utf-8", errors="ignore") as Qindex_file:
        Qindex_file.write(text)
#store the links in index.txt file

def add_text_to_folder(file_name, text):
    folder_path = os.path.join(QDATA_FOLDER, file_name)
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name + ".txt")
    with open(file_path, "w", encoding="utf-8", errors="ignore") as new_file:
        new_file.write(text)
#create a folder in folder and add txt file to it with name corresponding to index

def getPagaData(url, index):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, body_class)))
        time.sleep(1)
        heading = driver.find_element(By.CSS_SELECTOR, heading_class)
        body = driver.find_element(By.CSS_SELECTOR, body_class)
        #to wait until the page is loaded completely
        print(heading.text)
        if (heading.text):
            add_heading(heading.text)
            add_link(url)
            add_text_to_folder(str(index), body.text)
        time.sleep(1)
        return True
    except Exception as e:
        print(e)
        return False


arr = get_links()
for link in arr:
    success = getPagaData(link, index)
    if success:
        index += 1



driver.quit()