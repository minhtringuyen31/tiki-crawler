import requests
import time
import random
import pandas as pd
from tqdm import tqdm

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://tiki.vn/?src=header_tiki',
    'x-guest-token': '8jWSuIDBb2NGVzr6hsUZXpkP1FRin7lY',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

params = {
    'limit': '48',
    'include': 'sale-attrs,badges,product_links,brand,category,stock_item,advertisement',
    'aggregations': '1',
    'trackity_id': '70e316b0-96f2-dbe1-a2ed-43ff60419991',
    'category': '1883',
    'page': '1',
    'src': 'c1883',
    'urlKey':  'nha-cua-doi-song',
}

def parser_product_id(category, productId):
    d = dict()
    d['category'] = category
    d['product_id'] = productId
    return d

df_category = pd.read_csv('parent_category_data.csv')
print("Df Category: ", df_category)
cat = df_category.id.to_list()
print(cat)

product_id = []

for index, c in df_category.iterrows():
    print("Category", c)
    params['category'] = c.id
    params['src'] = c.src
    params['urlKey'] = c.urlKey
    for i in range(1, 11):
        params['page'] = i
        response = requests.get('https://tiki.vn/api/v2/products', headers=headers, params=params)#, cookies=cookies)
        if response.status_code == 200:
            print('request success!!!')
            for record in response.json().get('data'):
                id = record.get('id')
                print(c.id, id)
                print(parser_product_id(c.id, id))
                product_id.append(parser_product_id(c.id, id))
        time.sleep(random.randrange(3, 10))

df = pd.DataFrame(product_id)
df.to_csv('product_id_ver2.csv', index=False)
