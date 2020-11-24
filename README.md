# ptt_web_crawler
ptt beauty版網路爬蟲


Part 1.Installed module:
1.requests
2.requests_html
3.lxml
4.PyQuery
5.beautifulsoup4 (bs4)
6.urllib
7.time
8.requests.packages.urllib3

Part 2.環境:
windows 10+python 3.6 (anaconda spyder)

Part 3.注意事項:
對於每一個function都有計時器，會print出總執行時間(單位:秒)

Part 4.執行方法:
1.python web_crawler.py crawl
->爬下2020年到現在的所有ptt beauty版文章連結，存到all_articles.txt。並將其中所有熱門文章存入all_popular.txt
2.python web_crawler.py push start_date end_date (eg.python web_crawler.py push 304 609)
->數推文和噓文並找出前10名最會推跟噓的人(304代表3月4日，1020代表6月9日)
3.python web_crawler.py crawl popular start_date end_date (eg.python web_crawler.py popular 304 609)
->找爆文和圖片URL，並將結果輸出txt檔
4.python web_crawler.py crawl keyword {keyword} start_date end_date (eg.python web_crawler.py keyword 正妹 304 609)
->找內文中含有{keyword}的文章中的所有圖片
