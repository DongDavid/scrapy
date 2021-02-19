# scrapy 爬虫抓去动态渲染的网页数据  

## 初始化项目  

```sh
pip3 install scrapy 
pip3 install scrapy_splash

scrapy startproject jd
cd jd
scrapy genspider book 'https://book.jd.com/booksort.html' 
```

## 启动Splash服务  

```sh
# -d 表示后台运行 其实我还用nginx做了一个转发，所以我的调用地址实际上是https://xxx.xxx.com 而不是 http://127.0.0.1:8085 ，你们本地启动的话， 就直接用http://127.0.0.1:8085就好了,因为docker会把容器的8085端口映射到0.0.0.0的8085端口的
docker run -d -p 8050:8050 scrapinghub/splash
```
服务启动后，通过浏览器可以直接打开， 直接查看抓取网页的渲染效果(它会引用一些外部的js文件,可能会被墙，导致无法正常使用)

## 设置splash  

在`settings.py`文件中追加以下内容
```python
SPLASH_URL = 'https://splash.xxx.com'  
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
```


## 运行爬虫  

```sh
scrapy crawl book
```

## 结束战斗  

