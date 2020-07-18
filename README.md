# 网易云音乐歌单搜索爬虫

破解网易云音乐的加密 POST 提交请求，通过 Scrapy 实现的超快速多线程爬虫

具体介绍参考 

## 依赖

```shell
$ pip install -r requirements
```

## 功能

自定义关键词，爬取前 10 页歌单中的全部歌曲信息，并存入 MongoDB，每个 `Collection` 名称为歌单名，储存的内容格式如下：

| _id      | name   | time           | artists                           | album |
| -------- | ------ | -------------- | --------------------------------- | ----- |
| 自动生成 | 歌曲名 | 歌曲时长（ms） | 艺术家（多个艺术家直接用 / 分隔） | 专辑  |

## 使用方式

- 在 `settings.py` 中设置数据库信息

- 在工作目录下

  ```shell
  $ scrapy crawl playlist -a search_str={关键词}
  ```