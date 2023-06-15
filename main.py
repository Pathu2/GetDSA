# Import required packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Define the chromedriver service
s = Service('chromedriver.exe')

# Instantiate the webdriver
driver = webdriver.Chrome(service=s)

# The base URL for the pages to scrape
page_URL = "https://leetcode.com/problemset/all/?page="

def get_a_tags(URL):
    driver.get(URL)
    time.sleep(10)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    divs = soup.find_all('div', class_='truncate')
    ans = []
    for div in divs:
        a_tag = div.find('a')
        href = urljoin('https://leetcode.com/', a_tag['href'])
        ans.append(href)
    return ans

my_ans = []
for i in range(1, 55):
    my_ans = my_ans + get_a_tags(page_URL+str(i))

my_ans = list(set(my_ans))

#NOW WE WILL MAKE A txt FILE AND WILL SAVE THE HREF IN THAT, SUCH THAT EACH HREF ON 
# A NEW LINE.

# Open the text file in 'append' mode to add new content at the end of the file
with open('lc.txt', 'a') as file:
    for i in my_ans:
     file.write(i+'\n')

print(len(my_ans))