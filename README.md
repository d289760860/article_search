# article_search

#### 介绍
在中共江苏省委新闻网（https://www.zgjssw.gov.cn/yaowen/index_3.shtml）上检索一个时间范围内的新闻，并检查其中是否有省长或省委书记出现，若有则将时效内符合条件的新闻标题和链接按照时间从早到晚的顺序输出到文件中。

#### 环境

1.  python 3.7
2.  beautifulsoup 4.12.3
3.  requests 2.31

#### 安装教程

`conda create -n py37`

`conda activate py37`

`pip --default-timeout=100 install beautifulsoup4 -i https://pypi.tuna.tsinghua.edu.cn/simple`

`pip --default-timeout=100 install requests -i https://pypi.tuna.tsinghua.edu.cn/simple`

#### 使用说明

`python crawl.py`
