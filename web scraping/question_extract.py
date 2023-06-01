# for question name
# document.querySelector(".mr-2").innerHTML
# for question body
# document.querySelector(".px-5.pt-4").innerText
# document.querySelector(".mr-2.font-medium").innerText
# document.querySelector(".font-medium.capitalize").innerText

# Import required packages
import os
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

question_name = []
question_body = []
question_difficulty = []

def get_data_in_question(url):
    try:
      driver.get(url)
      time.sleep(3)
      question_name.append(driver.find_element(By.CSS_SELECTOR, ".mr-2.font-medium").text)
      print(question_name[-1])
      question_difficulty.append(driver.find_element(By.CSS_SELECTOR, ".font-medium.capitalize").text)   
      question_body.append(driver.find_element(By.CSS_SELECTOR, ".px-5.pt-4").text)
      return True
    except:
      print("Error in question: "+url)
      return False
    

    
lines = []
with open('lc.txt', 'r') as file:
    for line in file:
        lines.append(line.strip())
print("length of list",len(lines));    
question_no=0
e=[]
for j in range(0,len(lines)):
   i=lines[j]
   question_not_premium= get_data_in_question(i)
   if question_not_premium:
      question_no+=1
      with open('question_name.txt', 'a') as f:
         f.write(question_name[-1]+'\n')
         print(question_name[-1])
      with open('question_index_with_link.txt', 'a') as f:
         f.write(str(question_no)+'.'+i+'\n')
      with open('question_difficulty.txt', 'a') as f:
         f.write(question_difficulty[-1]+'\n')   
      # Create the main directory "Question_data" if it doesn't exist
      if not os.path.exists('Question_data'):
       os.mkdir('Question_data')
      # Create the subdirectory "1" inside "Question_data" if it doesn't exist
      if not os.path.exists(f'Question_data/{question_no}'):
       os.mkdir(f'Question_data/{question_no}')
      # Create the file "1.txt" inside the "1" folder and write content to it
      with open(f'Question_data/{question_no}/{question_no}.txt', 'w') as file:
          try:
           file.write(question_body[-1]+'\n')
          except:
           print("Error in finding body: ",i)
           e.append(i)
      question_name.clear()
      question_body.clear()
      question_difficulty.clear()
driver.quit()



   
