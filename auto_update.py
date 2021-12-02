import requests
from bs4 import BeautifulSoup 

url = 'https://dashboard.kerala.gov.in/covid/daily.php'
out = requests.get(url)
soup = BeautifulSoup(out.content, "html.parser")
table = soup.find("table", attrs={'class':'table-sm'})
rows = table.find_all('tr')
data = []
with open ("table.txt", "a") as f:
    for i in rows:
        table_data = i.findAll('td')
        td_data = [j.text for j in table_data]
        if len(td_data) > 0:
            data.append([td_data[0],td_data[1],td_data[2]])
            f.write(str(td_data[0]) + "," + str(td_data[1]) +"," + str(td_data[2]) + "\n")
    

    

