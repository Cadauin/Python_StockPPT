import json
import requests
from bs4 import BeautifulSoup as BS

Ptt_html_origin = ("https://www.ptt.cc/bbs/Stock/index.html")
data = []  # 儲存爬取到的資料

for i in range(3):
    Ptt_html=requests.get(Ptt_html_origin)
    P_soup= BS(Ptt_html.text,"html.parser")
    articles = P_soup.select('div.title a')
    paging=P_soup.select("div.btn-group-paging a")
    Ptt_html_origin="https://www.ptt.cc/"+paging[1]["href"]
    for L in articles :

        title = L.text
        link = "https://www.ptt.cc/" + L["href"]
        # 內容
        article_html = requests.get(link)
        article_soup = BS(article_html.text, "html.parser")
        # 日期
        date_elem = article_soup.select_one('div.date')
        date_text = date_elem.text.strip() if date_elem else ''
        # 作者
        author_elem = article_soup.select_one('div.author')
        author = author_elem.text.strip() if author_elem else ''
        # 推文
        content_elem = article_soup.select_one('#main-content')
        content = content_elem.text.strip() if content_elem else ''
        # 轉換為JSON格式
        data.append({
            'title': title,
            'link': link,
            'date': date_text,
            'author': author,
            'content': content
        })
        print(title,link,date_text,author,content)

# JSON檔
with open('ptt_stock.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)