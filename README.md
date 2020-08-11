# 网易云音乐歌单搜索爬虫

破解网易云音乐的加密 POST 提交请求，通过 Scrapy 实现的超快速多线程爬虫

具体介绍参考 [https://cyh.me/2020/07/music-163-com-crawler/](https://cyh.me/2020/07/music-163-com-crawler/)

## 依赖

```shell
$ conda install --file requirements.txt
```

## 功能

自定义关键词，爬取相关歌单中的全部歌曲信息，并存入 MongoDB，每个 `Collection` 名称为 `歌单名_歌单 id`，储存的内容格式如下：

| _id      | name   | time           | artists                           | album |
| -------- | ------ | -------------- | --------------------------------- | ----- |
| 歌曲 id | 歌曲名 | 歌曲时长（ms） | 艺术家（多个艺术家直接用 / 分隔） | 专辑  |

**注意：没有给登录 Cookie 只能获取前 20 个歌单；有 Cookie 则能获取最多 500 个歌单。**

## 使用方式

- 在 `music163com/settings.py` 中设置数据库信息

- 在 `main.py` 中设置搜索关键词 `search_str`

- 可选：在 `main.py` 中添加 Cookie 信息，需要先在网页登录，然后在 `music.163.com` 的 Cookie 中找到 `MUSIC_U` 的值填入

- 运行 `main.py`
