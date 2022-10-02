from flask import Flask
from flask_cors import CORS
from flask import request
from spider import *

app = Flask(__name__)
# 配置跨域
CORS(app, resources=r'/*')

# 获取所有分类
'''
请求方式:get
参数:无
返回值说明
    类型:json
    格式如下:
        {
            "玄幻": BASE_URL + "/dark.html",
            "都市": BASE_URL + "/city.html",
            "穿越": BASE_URL + "/cross.html",
            "网又": BASE_URL + "/games.html",
            "科幻": BASE_URL + "/unreal.html",
            "修真": BASE_URL + "/repair.html"
        }
'''


@app.route('/types')
def get_types():
    return types


# 获取一个类别的书单列表
'''
请求方式:get
参数:
    查询参数:无
    路径参数:str
返回值说明:
    类型:json字符串
    格式如下:
    [{'name': '斗罗大陆之终极斗罗', 'author': '唐家三少', 'url': 'https://www.um16.cn/info/8212.html'},...]
'''


@app.route('/type_list/<type_name>')
def type_list(type_name):
    url = types[type_name]
    return GetClassifiedBookList(url).get()


# 获取一本书的所有章节
'''
请求方式:post
请求体类型:json
请求体格式:
    {
        "url": "http...."
    }
返回值说明:
    类型:json字符串
    格式如下:
    [{'name': '第一章 那是什么？', 'url': 'https://www.um16.cn/info/8212/6218066.html'},...]
'''


@app.route('/chapters/', methods=["post"])
def get_chapters():
    url = request.json["url"]
    return GetDirectory(url).get()


# 获取一个章节的内容
'''
请求方式:post
请求体类型:json
请求体格式:
    {
        "url": "http...."
    }
返回值说明:
    类型:json字符串
    格式如下:
    {'title': ' 第十一章 魂力测试', 'content': '爸爸、妈妈，你们在说什么，我怎么听不懂？”蓝轩宇一脸好奇的看着父母...."}

'''


@app.route('/content', methods=["post"])
def get_content():
    url = request.json["url"]
    return GetContent(url).get()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5060)
