# Import required packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

# Define the chromedriver service
s = Service('chromedriver.exe')

# start webdriver
driver = webdriver.Chrome(service=s)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


page_URL = "https://codeforces.com/problemset/page/"


def get_a_tags(url):
    driver.get(url)
    time.sleep(5)
    links = driver.find_elements(By.TAG_NAME, "a")
    ans = []
    for i in links:
        try:
            if "/problemset/problem" in i.get_attribute("href"):
                ans.append(i.get_attribute("href"))
        except:
            pass
    ans = list(set(ans))
    return ans


my_ans = []
for i in range(1,88):
    my_ans += (get_a_tags(page_URL+str(i)))

my_ans = list(set(my_ans))

with open('cf.txt', 'a') as f:
    for j in my_ans:
        f.write(j+'\n')

# Print the total number of unique links found
print(len(my_ans))

# Close the browser
driver.quit()