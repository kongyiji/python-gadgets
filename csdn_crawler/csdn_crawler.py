import os
from goose3 import Goose
from goose3.text import StopWordsChinese
from bs4 import BeautifulSoup

url = 'https://www.csdn.net/nav/ops'

g = Goose({
    'stopwords_class': StopWordsChinese,
    'browser_user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
})
articles_urls = []
csdn_page = g.extract(url=url)

soup_csdn = BeautifulSoup(csdn_page.raw_html, 'lxml')

links = soup_csdn.find_all("h2")

for l in links:
    tmp_list = l.find_all('a')
    for t in tmp_list:
        link = t.get('href')
        articles_urls.append(link)
        print(link)


# print(articles_urls)

for url in articles_urls:
    article = g.extract(url=url)
    content = article.cleaned_text
    title = article.title.replace(os.sep, '&')
    with open('test' + os.sep + title + '.txt', 'w', encoding='utf-8') as f:
        f.write(content)
