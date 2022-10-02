## 这是一个笔趣阁的简单爬虫

### spider.py中封装了三个类：

- #### 	GetClassifiedBookList类实现了爬取对应分类下的书单列表

- ####     GetDirectory实现了爬取一本书的目录章节

- ####     GetContent实现了爬取某一本书某一章节的具体内容

### main.py是基于flask起的接口服务，实现了上述功能的几个接口

### 请求方式和返回值类型在代码中有详细的注释