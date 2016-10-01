# shanbay作业

[![Build Status](https://travis-ci.org/gaotongfei/shanbay.svg?branch=master)](https://travis-ci.org/gaotongfei/shanbay)
[![Code Health](https://landscape.io/github/gaotongfei/shanbay/dev/landscape.svg?style=flat)](https://landscape.io/github/gaotongfei/shanbay/dev)

## 开发环境:

* Mac OSX 10.11.6
* Python3.4.4
* travis 构建python 版本: 2.7, 3.3, 3.4, 3.5

```
$ virtualenv -p python3 venv
$ source venv/bin/activate && pip install -r requirements.txt

$ python manager.py db init && python manager.py migrate && python manager.py upgrade
$ python manager.py import_dict 

$ python manager.py runserver
```
