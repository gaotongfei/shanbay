# shanbay作业

## 开发环境:

* Mac OSX 10.11.6
* Python3.4.4

```
$ virtualenv -p python3 venv
$ pip install -r requirements.txt 

$ python manager.py db init && python manager.py migrate && python manager.py upgrade
$ python manager.py import_dict 

$ python manager.py runserver
```

## issues track && feature assignment:

* 笔记可为空(解决)
* 查看记的笔记
* 创建新笔记后的跳转问题(解决)
* 删除用户时, 用户提交的笔记无法cascade删除, 不过可以在程序逻辑上控制
