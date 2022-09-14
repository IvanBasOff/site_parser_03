import requests
import json
import time
import random



def get_page(page_num):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://www.wildberries.ru',
        'Referer': f'https://www.wildberries.ru/catalog/elektronika/smart-chasy?sort=popular&page={page_num}',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 YaBrowser/22.7.5.1027 Yowser/2.5 Safari/537.36',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Yandex";v="22"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    print(f'https://www.wildberries.ru/catalog/elektronika/smart-chasy?sort=popular&page={page_num}')
    response = requests.get(
        f'https://catalog.wb.ru/catalog/electronic6/catalog?appType=1&couponsGeo=12,3,18,15,21&curr=rub&dest=-1029256,-102269,-2162196,-1257786&emp=0&lang=ru&locale=ru&page={page_num}&pricemarginCoeff=1.0&reg=0&regions=68,64,83,4,38,80,33,70,82,86,75,30,69,22,66,31,40,1,48,71&sort=popular&spp=0&subject=787;1470;1514;2795;3211;3858;4031;7559',
        headers=headers)
    if response.status_code == 200:
        with open("index.html", "w", encoding='utf-8') as file:
            file.write(str(response.text))
        jresp = json.loads(response.text)
        #print(jresp)
    return jresp


def get_data_from_site(jresp):
    data_from_site = []
    data = jresp['data']
    products = data['products']
    for product in products:
        #print(product['name'])
        data_from_site.append({
            "name": product['name'],
            "brand": product['brand'],
            "sale": product['sale'],
            "old_price": product['priceU'],
            "new_price": product['salePriceU']
        })

    return data_from_site


def check_discounts(data, percent):
    new_data = []
    print(f'Всего до фильтрации: {len(data)}')
    for cur_data in data:
        #print(f"cur_data: {cur_data}")
        try:
            if cur_data['sale'] > percent:
                #print(f'SALE: {cur_data}')
                new_data.append(cur_data)
        except:
            print(f'Не нашлось скидки либо ошибка: {data}')
    print(f'Всего после фильтрации: {len(new_data)}')
    return new_data


def main():
    data = []
    max_req = 1
    for i in range(1, max_req+1):
        print(f"Опрос {i} из {max_req}...")
        jresp = get_page(i)
        data.extend(get_data_from_site(jresp))
        time.sleep(random.randrange(5, 10))

    data = check_discounts(data, percent=25)
    for d in data:
        print(d)


if __name__ == '__main__':
    main()
