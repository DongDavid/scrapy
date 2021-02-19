import scrapy
from scrapy_splash import SplashRequest


class BookSpider(scrapy.Spider):
    name = 'book'
    def start_requests(self):
        url = 'https://book.jd.com/booksort.html'
        splash_args = {"lua_source": """
                    --splash.response_body_enabled = true
                    splash.private_mode_enabled = false
                    splash:set_user_agent("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36")
                    assert(splash:go("__URL__"))
                    splash:wait(3)
                    return {html = splash:html()}
                    """}
        splash_args["lua_source"] = splash_args["lua_source"].replace("__URL__",url)

        yield SplashRequest(url, endpoint='run', args=splash_args, callback=self.jd)

    

    def jd(self, response):
        # 表达式其实可以借助chrome的开发者工具的copy-xpath生成
        data = response.xpath('//*[@id="booksort"]/div[2]/dl/dt/a/text()').extract()
        print("数据:")
        print(data)
        with open("./book.txt","w") as f:
            # 正则解析出来的数据
            f.write("".join(data))  # 自带文件关闭功能，不需要再写f.close()
         
        with open("./jd.html","w") as f:
            # 完整的网页记录到本地
            # 当正则取不到数据的时候， 先把爬取到的内容完整的写入文件， 
            # 然后看一下是否是未能爬到完整的数据， 如果有数据了再去看自己的正则表达式
            f.write("".join(response.xpath('//*').extract()))  # 自带文件关闭功能，不需要再写f.close()
         
        pass
