# API Server
![Python3.7](https://img.shields.io/badge/python-3.7-green.svg?style=flat-square&logo=python&colorB=blue)

项目简介...

此API使用Python 和 Flask 编写，通过标准的RESTFul接口传输数据。
## 快速上手
1. 克隆此仓库
```commandline
git clone https://github.com/yyywang/wuhan-api
cd wuhan-api
```
2. 安装依赖包
+ 若未安装 `pipenv` 先执行以下命令安装
```commandline
pip install pipenv
```
+ 通过 `pipenv` 自动安装依赖包
```commandline
pipenv shell
```
3. 添加敏感配置项

在以下位置新建 `secure.py` 文件
```
|-- app
    |-- config
        |-- secure.py
```
在 `secure.py` 文件中添加数据库连接与腾讯地图API配置项
+ 数据库连接
```python
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://{user}:{password}@localhost/{database-name}'
```
+ 腾讯地图接口 TX_MAP_KEY ([接口使用指南](https://lbs.qq.com/guides/startup.html))
```python
TX_MAP_KEY = '...'
```

4. 运行
```commandline
puthon wuhan.py
```
此时服务应该成功运行在 `http://localhost:5000`。参考 [api文档](api_guide.md) 查看已开发接口。
> 参考手册： [错误码](code.md)


----


# 待办

- 缓存优化
- 数据库索引优化
- 腾讯地图位置查询限制 200
