import requests
from bs4 import BeautifulSoup
import urllib3
import pymysql

headers = {'login_username': 'username',
           'login_password': 'password'}

url = 'https://wiki-sd.homecredit.ru/doku.php?id=group:servicedesk:marshrutizatsiya'
ssl = urllib3.disable_warnings()
response = requests.get(url=url, verify=False, auth=(headers['login_username'], headers['login_password']))
soup = BeautifulSoup(response.text, "html.parser")

container = soup.select_one("div.table-responsive")

products = container.find_all("tr")

args = []
for product in products:
    headers = {'login_username': 'username',
               'login_password': 'password'}
    url = 'https://wiki-sd.homecredit.ru/doku.php?id=group:servicedesk:marshrutizatsiya'
    ssl = urllib3.disable_warnings()
    response = requests.get(url=url, verify=False, auth=(headers['login_username'], headers['login_password']))
    soup = BeautifulSoup(response.text, "html.parser")
    Name = product.select_one("td.col0")
    if Name is not None:
        Name = Name.text
    else:
        Name = ''
    Worker = product.select_one("td.col1")
    if Worker is not None:
        Worker = Worker.text
    else:
        Worker = ''
    Sample = product.select_one("td.col2")
    if Sample is not None:
        Sample = Sample.text
    else:
        Sample = ''
    Disc = product.select_one("td.col3")
    if Disc is not None:
        Disc = Disc.text
    else:
        Disc = ''
    args.append((Name, Worker, Sample, Disc))

conn = pymysql.connect(host='localhost', port=3306, user='root', password='', db='nicetry')
cursor = conn.cursor()
row = cursor.execute("truncate marsh")
row1 = cursor.executemany("insert into marsh(Name, Worker, Sample, Disc)values(%s, %s, %s, %s)", args)

conn.commit()
cursor.close()
conn.close()