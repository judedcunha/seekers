import requests
from bs4 import BeautifulSoup
import urllib.request
import zipfile

# Make a request
page = requests.get(
    "http://www.missingpersonhelpline.org/missing-person.php?splid=706b947eccc0afa30f5131a0fa2fd473")
soup = BeautifulSoup(page.content, 'html.parser')
test = soup.select('div#search.container > div.row.page > div.col-md-12.col-sm-12 > table > tr > td > table > tr > td:nth-of-type(2) ' )
for i in range(len(test)):
    print(i)
    print(test[i].get_text())

opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

filename = test[0].get_text()+'.jpg'
image_url = "https://www.missingpersonhelpline.org/photos/"+test[0].get_text()+"_1.jpg"
print(image_url)

urllib.request.urlretrieve(image_url, filename)


zipfile.ZipFile(test[0].get_text()+'.zip', mode='w').write(filename,test[0].get_text()+"\\"+filename, zipfile.ZIP_DEFLATED)








#http://www.missingpersonhelpline.org/photos/161341016681_1.jpg