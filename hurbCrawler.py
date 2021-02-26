import csv
import requests
from bs4 import BeautifulSoup
import getEachPages

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
}


def get_new_csv(path='medicineTable.csv'):
    return open(path, 'w', newline="", encoding='utf-8-sig')


csv_file = get_new_csv()
csv_write = csv.writer(csv_file)

for page in range (1, 46):
    dbEntry = []
    page_url = 'http://www.zhongyoo.com/name/page_'+ str(page) + '.html'
    res = requests.get(page_url, headers=headers)
    res.encoding = 'GBK'
    soup = BeautifulSoup(res.text, 'lxml')

    try:
        medicines = soup.find('div', {'class': 'r2-con'}).find_all('div', {'class': 'sp'})

        for medicine in medicines:
            url = medicine.find('a').get('href')
            dbEntry.append(getEachPages.getByURL(url))

    except AttributeError as e:
        print('Error!', e)
        continue

    for Entry in dbEntry:
        if (not len(Entry) == 0) and (not len(Entry.get('Name')) == 0):
            writerow = [Entry.get('Name')]
            for key in Entry.keys():
                if not key == 'Name':
                    writerow.append(key)
                    writerow.append(Entry.get(key))
            if not len(writerow) == 0:
                csv_write.writerow(writerow)


