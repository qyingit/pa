# -*- coding:utf-8 -*-
import requests
import bs4

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    "content-type": "text/html",
    "vary": "Accept-Encoding",
}



def test_content(content_url):
    data = requests.get(content_url)
    encoding = assert_encoding(data)
    encode_content = data.content.decode(encoding, 'replace').encode('utf-8', 'replace')
    soup = bs4.BeautifulSoup(encode_content, 'html.parser')
    div = soup.find('div', attrs={'class': 'page'})
    test_one_page(content_url)
    for page in div.find_all('a', attrs={'class': ''}):
        url ='%s%s%s%s'%('https://cq.newhouse.fang.com', page['href'],'?ctm=1.cq.xf_search.page.',page.string)
        test_one_page(url)



def test_one_page(url):
    data = requests.get(url)
    encoding = assert_encoding(data)
    encode_content = data.content.decode(encoding, 'replace').encode('utf-8', 'replace')
    soup = bs4.BeautifulSoup(encode_content, 'html.parser')
    div = soup.find('div', attrs={'class': 'nl_con clearfix'})
    # 获取四个楼盘的div，更具他们的class = "tenrtd"
    for house in div.find_all('div', attrs={'class': 'nlc_details'}):
        # 根据class="text1"获取存储楼盘标题的div
        titleDiv = house.find('div', attrs={'class': 'nlcd_name'})
        title = titleDiv.find('a').get_text().strip()
        # 根据class="text2"获取存储楼盘价格的地址
        addressDiv = house.find('div', attrs={'class': 'address'})
        address = addressDiv.find('a')['title']
        fang = title + "\t\t" + address
        print fang
        # price = priceDiv.find('b').text


def assert_encoding(response):
    if response.encoding == 'ISO-8859-1':
        encodings = requests.utils.get_encodings_from_content(response.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = response.apparent_encoding
    return encoding



if __name__ == '__main__':
    #巴南
    #content_url = "https://cq.newhouse.fang.com/house/s/banan/?ctm=1.cq.xf_search.lpsearch_area.8#no"
    #渝北
    #content_url = "https://cq.newhouse.fang.com/house/s/yubei/?ctm=1.cq.xf_search.lpsearch_area.4"
    #南岸
    #content_url = "https://cq.newhouse.fang.com/house/s/nanan/?ctm=1.cq.xf_search.lpsearch_area.5"
    #沙坪坝
    #content_url = "https://cq.newhouse.fang.com/house/s/shapingba/?ctm=1.cq.xf_search.lpsearch_area.6"

    #other
    other_content_url = "https://cq.newhouse.fang.com/house/s/yubei/a9%D6%D0%D1%EB%B9%AB%D4%B0/?ctm=1.cq.xf_search.lpsearch_area.4"
    test_content(other_content_url)

