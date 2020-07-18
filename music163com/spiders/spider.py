import json
import scrapy
from scrapy import FormRequest
from .encrypt_post import Encrypt_music163com
from ..items import Music163ComItem


Encrypt = Encrypt_music163com()


class Music163ComSpider(scrapy.spiders.Spider):
    name = "playlist"  # 搜索网易云歌单并保存相关信息
    allowed_domains = ["music.163.com"]

    def __init__(self, search_str):
        super(Music163ComSpider, self).__init__()
        self.search_str = search_str

    def start_requests(self):
        search_url = "https://music.163.com/weapi/cloudsearch/get/web"
        # 总共能获取 10 页搜索结果
        for i in range(10):
            # 构造提交数据形式，下同
            post_data = (
                '{{"hlpretag":"<span class=\\"s-fc7\\">","hlposttag":"</span>","s":"{}","type":"1000","offset":"{}",'
                '"total":"true","limit":"30","csrf_token":""}}'.format(
                    self.search_str, i * 30
                )
            )
            # POST 提交，下同
            yield FormRequest(
                url=search_url,
                formdata=Encrypt.encrypt(post_data),
                callback=self.search_parse,
            )

    def search_parse(self, response):
        playlist_url = "https://music.163.com/weapi/v6/playlist/detail"

        search_detail = json.loads(response.text)
        # 获取搜索结果中的歌单信息
        playlists = search_detail["result"]["playlists"]

        for playlist in playlists:
            post_data = '{{"id":"{}","offset":"0","total":"true","limit":"1000","n":"1000","csrf_token":""}}'.format(
                playlist["id"]
            )
            yield FormRequest(
                url=playlist_url,
                formdata=Encrypt.encrypt(post_data),
                callback=self.playlist_parse,
            )

    def playlist_parse(self, response):
        song_url = "https://music.163.com/weapi/v3/song/detail"

        playlist_detail = json.loads(response.text)["playlist"]
        # 获取歌单名和歌单中的歌曲信息
        title = playlist_detail["name"]
        songs = playlist_detail["trackIds"]

        for song in songs:
            post_data = '{{"id":"{0}","c":"[{{\\"id\\":\\"{0}\\"}}]","csrf_token":""}}'.format(
                song["id"]
            )
            # meta 标记歌曲所属的歌单
            yield FormRequest(
                url=song_url,
                formdata=Encrypt.encrypt(post_data),
                callback=self.song_parse,
                meta={"playlist_title": title},
                dont_filter=True,
            )

    def song_parse(self, response):
        # 解析歌单名
        playlist_title = response.meta["playlist_title"]

        song_detail = json.loads(response.text)["songs"][0]
        # 获取歌曲各项信息
        name = song_detail["name"]
        time = song_detail["dt"]
        artists = " / ".join(map(lambda x: x["name"], song_detail["ar"]))  # 多个创作者用 / 分开
        album = song_detail["al"]["name"]

        # 制作 item
        item = Music163ComItem()
        item["playlist_title"] = playlist_title
        item["name"] = name
        item["time"] = time
        item["artists"] = artists
        item["album"] = album

        yield item
