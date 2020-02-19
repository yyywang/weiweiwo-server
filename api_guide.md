# 1. 概述

+ base_url：`{domain}/v1/`
+ 可选参数：`*` 标记

# 2. API

## 1. seek-help

| 序号 | url                  | type   | 参数                                                         | 作用         | 返回值       | 是否需登录 | 备注                              |
| ---- | -------------------- | ------ | ------------------------------------------------------------ | ------------ | ------------ | ---------- | --------------------------------- |
| 1    | seek-help            | post   | cat_num/dog_num/end_date/address/latitude/longitude/addressName/traffic_control/phone/wx_id | 发布求助信息 | APIException | N          | cat_num 与 dog_num 二者至少填一个 |
| 2    | seek-help/\<int:id\> | delete |                                                              | 删除求助信息 | APIException |            |                                   |

## 2. rescue



| 序号 | url               | type | 参数                                | 作用                            | 返回值 | 是否需登录 | 备注                                                         |
| ---- | ----------------- | ---- | ----------------------------------- | ------------------------------- | ------ | ---------- | ------------------------------------------------------------ |
| 1    | rescue/position   | get  | \*page/\*province/\*city/\*district | 获取求助信息列表，通过位置筛选  |        | N          |                                                              |
| 2    | rescue/distance   | get  | latitude/longitude                  | 获取求助信息列表，距离由近到远  |        | N          |                                                              |
| 3    | rescue/search     | get  | q                                   | 搜索求助帖，支持地址/手机号搜索 |        | N          |                                                              |
| 4    | rescue/feedback   | post | msg_id/error_type                   | 求助信息错误反馈                |        | N          | err_type： 0 - 联系不上宠物主；1 - 宠物已不需要帮助；2 - 信息重复；3 - 其他 |
| 5 | rescue/\<int:id\> | get |  | 返回id=id的 SeekHelp数据 | | N |  |
| 6   | rescue/\<int:id\> | put  | end_date/help_date               | 更新求助信息                    |        | N          |                                                              |
