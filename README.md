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

# token

eyJhbGciOiJIUzUxMiIsImlhdCI6MTU4MjAxNjIwNiwiZXhwIjoxNTg0NjA4MjA2fQ.eyJ1aWQiOjMsInR5cGUiOjIwMCwic2NvcGUiOiJVc2VyU2NvcGUifQ.wnPImsHxGZGvH38mVgr4QKOCh4h9eZzU3FRn9jj8fzMeUqfHB-3D_eJ1U-xnNGO-nZj8nInZzqt_apDx-VZ7rQ

# 未完成功能

1. 服务端配置生成小程序二维码接口
2. 数据库建立字段索引优化查询
3. 数据库缓存优化
    - `GET  /v1/seek-help/\<int:id\>/boost <statistics>字段`

# 备注
## 1. 首页数据性能问题
1. 按助力等级（高、中、低）分类所有求助信息
2. 获取该用户位置与所有求助信息地点的距离（调用腾讯地图接口实现）
3. 按公式（计算排序值=0.4*几天后需要帮助+0.6距离我多远，按从小到大排序）排序每个等级的数据



# 待办

1. 订阅消息通知
2. 缓存优化
3. 数据库索引优化
4. 腾讯地图位置查询限制 200
