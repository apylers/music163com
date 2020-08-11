from scrapy import cmdline

search_str = "中文"
cmdline.execute("scrapy crawl playlist -a search_str={}".format(search_str).split())
