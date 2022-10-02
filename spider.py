from wsgiref import headers

import requests
from bs4 import BeautifulSoup
from copyheaders import headers_raw_to_dict

# 从浏览器的赋值的请求头
row_headers = b'''
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate, br
Accept-Language: zh,zh-CN;q=0.9,en;q=0.8
Cache-Control: no-cache
Connection: keep-alive
Cookie: fikker-M0cL-shyZ=GdyMMXsdN8L6A8kFITQLiI7fY2IrcncI; fikker-M0cL-shyZ=GdyMMXsdN8L6A8kFITQLiI7fY2IrcncI; Hm_lvt_f4f67ed343c83044d7908f39f0517ee7=1664691565; fikker-FqLS-laX3=Rm4OTErmvmTmVg8w6L0mVKrSpUPAdqDU; fikker-FqLS-laX3=Rm4OTErmvmTmVg8w6L0mVKrSpUPAdqDU; Hm_lpvt_f4f67ed343c83044d7908f39f0517ee7=1664696104
Host: www.um16.cn
Pragma: no-cache
Referer: https://www.um16.cn/dark.html
sec-ch-ua: "Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36
'''
# 将请求头转换为字典格式
headers = headers_raw_to_dict(row_headers)
# 笔趣阁网址
BASE_URL = "https://www.um16.cn"
# 笔趣搁的6分类
types = {
    "玄幻": BASE_URL + "/dark.html",
    "都市": BASE_URL + "/city.html",
    "穿越": BASE_URL + "/cross.html",
    "网又": BASE_URL + "/games.html",
    "科幻": BASE_URL + "/unreal.html",
    "修真": BASE_URL + "/repair.html"
}
# 设置响应的编码格式,因为是中文的,所以设置为gbk
encoding = "gbk"
# BeautifulSoup的解析方式
parser = "html.parser"


# 获取对应分类的书单
class GetClassifiedBookList:
    def __init__(self, url: str):
        self.url = url

    def get(self):
        res = requests.get(url=self.url, headers=headers)
        res.encoding = encoding
        soup = BeautifulSoup(res.text, parser)
        selector = "#newscontent > div.r > ul"
        books = soup.select_one(selector).find_all("li")

        book_list = []
        for book in books:
            a = book.find("a")
            url = a["href"]
            name = a.text
            author = book.find_all("span")[1].text
            info = {
                "name": name,
                "author": author,
                "url": url
            }
            book_list.append(info)
        return book_list


# 获取某一本书的目录章节
class GetDirectory:
    def __init__(self, url: str):
        self.url = url

    def get(self):
        res = requests.get(url=self.url, headers=headers)
        res.encoding = encoding
        soup = BeautifulSoup(res.text, parser)
        selector = "#list > dl"
        chapters = soup.select_one(selector).find_all('dd')
        chapter_list = []
        for chapter in chapters:
            chapter_url = chapter.find("a")["href"]
            chapter_name = chapter.find("a").text
            chapter_list.append({
                "name": chapter_name,
                "url": "https://www.um16.cn" + chapter_url
            })
        return chapter_list


# 获取一个章节的具体内容
class GetContent:
    def __init__(self, url: str):
        self.url = url

    def get(self):
        res = requests.get(url=self.url, headers=headers)
        res.encoding = encoding
        soup = BeautifulSoup(res.text, parser)
        title_selector = "#wrapper > div.content_read > div > div.bookname > h1"
        content_selector = "#content"
        title = soup.select_one(title_selector).text
        content = soup.select_one(content_selector).text
        return {
            "title": title,
            "content": content
        }


if __name__ == '__main__':
    print(GetClassifiedBookList(types["玄幻"]).get())
    print(GetDirectory("https://www.um16.cn/info/8212.html").get())
    print(GetContent("https://www.um16.cn/info/8212/6218076.html").get())
