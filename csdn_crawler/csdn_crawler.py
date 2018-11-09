import os
import requests
from bs4 import BeautifulSoup

# OPS页面地址
csdn_url = 'https://www.csdn.net/nav/ops'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
articles_urls = []


def soup_url(url):
    page = requests.get(url, headers = headers)
    return BeautifulSoup(page.text, "lxml")

soup_csdn = soup_url(csdn_url)
links = soup_csdn.find_all("h2")

# 获取文章地址
for l in links:
    tmp_list = l.find_all('a')
    for t in tmp_list:
        link = t.get('href')
        articles_urls.append(link)
        print(link)


# print(articles_urls)
# 获取文章内容
for url in articles_urls:
    soup = soup_url(url)
    content = soup.find_all(class_ = 'article_content')[0].get_text()
    title_raw = soup.find_all(class_ = 'title-article')[0].get_text()
    title = title_raw.replace('/', '&')
    with open('test' + os.sep + title + '.txt', 'w', encoding='utf-8') as f:
        f.write(content)
