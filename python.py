import requests #J个是请求模块
import parsel #数据筛选(xml, re, bs4) 👉"bs4"这东西🐕都不用好久没更新了🤭 7年左右没更了！
import os

url = "https://www.jdlingyu.com/tuji" #网页链接
response = requests.get(url) #1.发送网络请求
# print(response.text) #打印获取到的内容
html_data = response.text #2.获取数据网页代码
selector = parsel.Selector(html_data) #3.筛选数据
url_list = selector.xpath('//div[@class="post-info"]/h2/a/@href').getall()
# print(url_list)
for detail_url in url_list: #4.发送网络请求到相册页面
    # print(detail_url)
    detail_html = requests.get(detail_url).text
    # print(detail_html)
    detail_selector = parsel.Selector(detail_html) #5.筛选数据 图片地址
    title = detail_selector.xpath('//h1/text()').get()
    print('正在爬取：{title}') #爬取标题
    if not os.path.exists('img/' + title): 
        os.mkdir('img/' + title)
    img_list = detail_selector.xpath('//div[@class="entry-content"]/p/img/@src').getall() #批量爬取页面里的图片
    for img in img_list:
        img_data = requests.get(img).content
        img_title = img.split('/')[-1]
        with open(f'img/{title}/{img_title}', mode='wb') as f:
            f.write(img_data)
        print('正在爬取：{img_title}')
