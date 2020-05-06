from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime

f = open("info.data", "r")
fLines = f.readlines()
f.close()
inputData = []
for line in fLines:
    tmp = line.strip().split(': ')
    inputData.append(tmp[1])
eid = inputData[0]
password = inputData[1]
semester_id = inputData[2]
ignore = inputData[3].split(',')
class_ids = inputData[4].split(',')

initUrl = 'https://utdirect.utexas.edu/apps/registrar/course_schedule/{}/'.format(semester_id)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu') 

driver = webdriver.Chrome(options=options)
driver.get(initUrl)
driver.find_element_by_id("IDToken1").send_keys(eid)
driver.find_element_by_id("IDToken2").send_keys(password)
button = driver.find_element_by_name('Login.Submit')
button.click()

for i in range(0, 100):
    output = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    output += 'Last Updated: {}\n'.format(datetime.now().strftime("%I:%M:%S %p"))
    for class_id in class_ids:
        driver.get("{}{}/".format(initUrl, class_id))
        content = driver.page_source
        soup = BeautifulSoup(content, 'lxml')
        table_rows = soup.find('table', id='details_table').find_all('tr')
        data = table_rows[1].find_all('td')
        data = [i.text for i in data]
        status = data[5] in ignore
        notif = "" if status else "<-------- REGISTER NOW !!!!!!!!!!"
        buffer = "" if status else "--------->"
        output += "{buff} | {id} | {prof} | {status} | {attention}\n".format(
            id=data[0].strip(), days=data[1].strip(), time=data[2].strip(), 
            room=data[3].strip(), prof=data[4].strip(), status=data[5].strip(),
            flags = data[6].strip(), buff = buffer, attention=notif)
    print(output)
    sleep(5)
    
