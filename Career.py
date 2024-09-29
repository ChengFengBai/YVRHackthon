import requests # type: ignore
from bs4 import BeautifulSoup  # type: ignore
import csv

def scrape_page(soup, info):
    info_element=soup.find_all('div', class_='bc-groups')
    for element in info_element:
        all_info=element.find('div', class_='bc-bar-inner dw-circlex focus')
        for item in all_info:
            style=item.get('style','')

            if 'left: 80.4872%' in style and 'background: rgb(159, 41, 255)' in style:
                happy_rating=item.find('div', 'span', class_='bc-bar-label chart-text value label').text.strip()
            if 'left: 55.61%' in style and 'background: rgb(49, 202, 168)' in style:
                impact_rating = item.find('div', 'span', class_='bc-bar-label chart-text value label').text.strip()
            if 'left: 86.0482%' in style and 'background: rgb(6, 166, 238)' in style:
                pay_adequacy = item.find('div', 'span', class_='bc-bar-label chart-text value label').text.strip()
    info_lable=soup.find_all('div', class_='bc-row-label row-label chart-text label')
    for element in info_lable:
        job_rating=element.find('span').text
        info.append(
            {
            'Job':job_rating,
            'Happy':happy_rating,
            'Impact':impact_rating,
            'Pay Adequacy':pay_adequacy
            }
        )

url='https://today.yougov.com/economy/articles/45927-americans-rank-30-occupations-pay-happiness-impact'
headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0'
}
page=requests.get(url, headers=headers)
soup=BeautifulSoup(page.text, 'html.parser')
info=[]
scrape_page(soup, info)

csv_data=open('data.csv', 'w', encoding='utf-8', newline='')
writer=csv.writer(csv_data)
writer.writerow(['Job','Happy','Impact','Pay Adequacy'])
for info in info:
    writer.writerow(info.values())
csv_data.close()