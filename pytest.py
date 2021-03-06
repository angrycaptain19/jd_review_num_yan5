import os
import re
import csv
import random
from datetime import datetime
import requests
import time


log = open(f'./result/r_{(time.time())*10000}.txt', 'w')
url = 'https://club.jd.com/comment/skuProductPageComments.action?callback=fetchJSON_comment98&productId={0}&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'

filename = os.path.dirname(os.path.realpath(__file__))+'/useragents.csv'
user_agent_csv = open(filename, 'r')
reader = csv.reader(user_agent_csv)
user_agent_list = [row for row in reader]

def random_ua():
    return random.choice(user_agent_list)[0]

def fetch(sku):
    skus = sku.split(',')
    sku_n,snapshot_day = skus[0],skus[1]
    sku_m = sku_n.replace('JD_','')
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
        'Referer': f'https://item.jd.com/{sku_m}.html',
        'User-Agent': random_ua()
    }
    r = requests.get(url.format(sku_m), headers=header).text
    commentCount = re.match('.*"commentCount":(\d+).*', r)
    defaultGoodCount = re.match('.*"defaultGoodCount":(\d+).*', r)
    goodCount = re.match('.*"goodCount":(\d+).*', r)
    generalCount = re.match('.*"generalCount":(\d+).*', r)
    poorCount = re.match('.*"poorCount":(\d+).*', r)
    videoCount = re.match('.*"videoCount":(\d+).*', r)
    afterCount = re.match('.*"afterCount":(\d+).*', r)
    if commentCount and commentCount.groups():
        print(sku_n,commentCount)
        log.write(f'''{sku_n},{snapshot_day},{commentCount[1]},{defaultGoodCount[1]},{goodCount[1]},{generalCount[1]},{poorCount[1]},{videoCount[1]},{afterCount[1]}\n''')
    else:
        print(sku_n)

def main():
    skus = []
    with open('list.txt', 'r') as f:
        for line in f:
            skus.append(line.replace('\n',''))

    # log.write(f'starts at: {datetime.now()}\n')
    print(f'starts at: {datetime.now()}')
    for s in skus:
        try:
            fetch(s)
        except:
            # log.write(f'error at: {datetime.now()}\n')
            return
    print(f'ends at: {datetime.now()}')
    # log.write(f'ends at: {datetime.now()}\n')

if __name__ == '__main__':
    main()
