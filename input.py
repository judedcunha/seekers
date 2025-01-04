from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import urllib.request
import zipfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.common.exceptions import NoSuchElementException
import time

def check_element():
	try:
		driver.find_element_by_name("linkentered")
		return 1
	except StaleElementReferenceException:
		print("Element does not exist")
		return 0
	except NoSuchElementException:
		print("Element does not exist")
		return 0




driver = webdriver.Firefox()
driver.get("http://192.168.5.58:5000/index")
while(1):
	#print(driver.find_element_by_name("linkentered"))
	#checkbox=driver.find_element_by_name("linkentered")
	if(check_element()):
		try:
			if(driver.find_element_by_name("linkentered").is_selected()):
				linktomp = driver.find_element_by_name("link")
				print(linktomp.get_attribute('value'))
				page = requests.get(linktomp.get_attribute('value'))
				soup = BeautifulSoup(page.content, 'html.parser')
				test = soup.select('div#search.container > div.row.page > div.col-md-12.col-sm-12 > table > tr > td > table > tr > td:nth-of-type(2) ' )
				for i in range(len(test)):
				    print(test[i].get_text())




				opener=urllib.request.build_opener()
				opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
				urllib.request.install_opener(opener)

				filename = test[0].get_text()+'.jpg'
				image_url = "https://www.missingpersonhelpline.org/photos/"+test[0].get_text()+"_1.jpg"
				print(image_url)

				urllib.request.urlretrieve(image_url, filename)


				zipfile.ZipFile(test[0].get_text()+'.zip', mode='w').write(filename,test[0].get_text()+"\\"+filename, zipfile.ZIP_DEFLATED)






				#input automation
				inputElement = driver.find_element_by_name("aadhar")
				inputElement.send_keys(test[0].get_text())
				# inputElement.send_keys(Keys.ENTER)

				inputElement = driver.find_element_by_name("name")
				inputElement.send_keys(test[1].get_text())
				# inputElement.send_keys(Keys.ENTER)

				inputElement = driver.find_element_by_name("fname")
				inputElement.send_keys(test[2].get_text())
				# inputElement.send_keys(Keys.ENTER)

				inputElement = driver.find_element_by_name("gender")
				inputElement.send_keys(test[3].get_text())
				# inputElement.send_keys(Keys.ENTER)


				inputElement = driver.find_element_by_name("rplace")
				inputElement.send_keys(test[5].get_text())
				# inputElement.send_keys(Keys.ENTER)


				inputElement = driver.find_element_by_name("date_missing")
				inputElement.send_keys(test[7].get_text())
				# inputElement.send_keys(Keys.ENTER)


				inputElement = driver.find_element_by_name("place_missing")
				inputElement.send_keys(test[8].get_text())
				# inputElement.send_keys(Keys.ENTER)


				inputElement = driver.find_element_by_name("weight")
				inputElement.send_keys(test[10].get_text())
				# inputElement.send_keys(Keys.ENTER)



				inputElement = driver.find_element_by_name("Build")
				inputElement.send_keys(test[12].get_text())
				# inputElement.send_keys(Keys.ENTER)


				inputElement = driver.find_element_by_name("height")
				inputElement.send_keys(test[9].get_text())
				# inputElement.send_keys(Keys.ENTER)

				inputElement = driver.find_element_by_name("Complexion")
				inputElement.send_keys(test[11].get_text())
				# inputElement.send_keys(Keys.ENTER)


				inputElement = driver.find_element_by_name("age")
				inputElement.send_keys(test[4].get_text())
				# inputElement.send_keys(Keys.ENTER)


				# inputElement = driver.find_element_by_name("Hair")
				# inputElement.send_keys(test[4].get_text())


				#uploading files
				inputElement = driver.find_element_by_xpath("//input[@name='pfile']")
				inputElement.send_keys("C:\\Users\\FIREC\\Desktop\\project1\\"+test[0].get_text()+".jpg")


				inputElement = driver.find_element_by_xpath("//input[@name='file']")
				inputElement.send_keys("C:\\Users\\FIREC\\Desktop\\project1\\"+test[0].get_text()+".zip")

				driver.find_element_by_xpath("//input[@id='linkenteredid']").click()
		except:
			print("Trying again")
			driver.get("http://192.168.0.127:5000/index")
				# Make a request
				
			
			



