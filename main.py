from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

def get_info(soup, item_data):    
    items = soup.find_all('li', class_='result-lots__item')    
    for item in items:
        item_dict = {}

        name_tag = item.find('div', class_='title-v2 result-lots__title')
        item_dict['name'] = name_tag.get_text() if name_tag else None

        info_values = item.find_all('dd', class_='result-lots__data-desc')
        item_dict['info'] = [info.get_text().strip().replace("\n", "") for info in info_values] if info_values else None

        url_tag = item.find('a', class_='result-lots__link-title')
        item_dict['url'] = "https://sca.auction/" + url_tag.get('href') if url_tag else None

        status_tag = item.find ('p', class_='timer-v2__time lot-status__time') 
        item_dict['status'] = status_tag.get_text().strip() if status_tag else None

        price_tag = item.find('span', class_="result-lots__price-value")
        item_dict['price'] = price_tag.get_text().strip() if price_tag else None

        item_data.append(item_dict)

def main(start_page, end_page):
    item_data = []

    for i in range(start_page, end_page + 1):
        URL = f"https://sca.auction/en/search/type-cars/year-2014-2024/page-{i}"

        website = requests.get(URL, headers=HEADERS)
        website.encoding = 'UTF-8'
        time.sleep(2)
        doc = BeautifulSoup(website.content, 'html.parser')

        get_info(doc, item_data)

    for item in item_data:
        print("Name:", item['name'])
        print("Status:", item['status'])
        print("Info:", item['info'])
        print("Price:", item["price"])
        print("Url:", item['url'])
        print("\n")

    columns = ['name', 'status', 'info', 'price', 'url']
    df = pd.DataFrame(item_data, columns=columns)
    df.to_excel('Auction_list.xlsx', index=False)

if __name__ == "__main__":
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 OPR/104.0.0.0'
    }

    start_page = 1
    end_page = 300
    main(start_page, end_page)
