# https://github.com/soroush44d/Poetry-Scraping-Script-

import requests
from bs4 import BeautifulSoup as bfs

''' 
print('Select Your CHoice:\n 1)divan Shams \n 2)Ghazaliat Saadi\n 3)Robaee Khayam\n 4)robaei Saadi\n 5)Ghazal Hafez\n 6)Nezami Khosro Shirin\n 7)Dehlavi Ghazaliat\n 8)Attar Ghazaliat')
choice = int(input('Enter :'))

if choice == 1:
    url = 'https://ganjoor.net/moulavi/shams/ghazalsh'

if choice == 2:
    url = 'https://ganjoor.net/saadi/divan/ghazals'

if choice == 3:
    url = 'https://ganjoor.net/khayyam/robaee'

if choice == 4:
    url = 'https://ganjoor.net/saadi/divan/robaees'

if choice == 5:
    type = 'ghazal'
    poet_name = 'hafez'
    url = f'https://ganjoor.net/{poet_name}/{type}'

if choice == 6:
    url = 'https://ganjoor.net/nezami/5ganj/khosro-shirin'

if choice == 7:
    url = 'https://ganjoor.net/khosro/gozide/ghazalamkh'

if choice == 8:
    url = 'https://ganjoor.net/attar/divana/ghazal-attar'
''' 

url = 'https://ganjoor.net/moulavi/shams/ghazalsh'

response = requests.get(url)

content = bfs(response.text, 'html.parser')
print(content)
#exit()
page_counts = len(content.find_all('p', class_='poem-excerpt'))

for page_number in range(page_counts):
    link =url+'/sh'+str(page_number+1)
    print(link)
    response = requests.get(link)
    content = bfs(response.text, 'html.parser')

    count = len(content.find_all('div', class_='b'))
    for i in range(count):
        id = 'bn'+str(i+1)
        a = content.find_all('div', class_='b', attrs={'id': id})
        if len(a) != 0:
            mesra_aval = a[0].find('div', class_='m1').text
            mesra_dovom = a[0].find('div', class_='m2').text
            with open('hafez.txt', 'a', encoding='utf-8') as file:
                file.write('|'+mesra_aval+'         '+mesra_dovom)
                file.write('\n')
        else:
            continue