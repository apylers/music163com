from scrapy import cmdline

MUSIC_U = (
    ""
)
search_str = "kksk"
cmdline.execute(
    "scrapy crawl playlist -a search_str={} -a MUSIC_U={}".format(
        search_str, MUSIC_U
    ).split()
)
