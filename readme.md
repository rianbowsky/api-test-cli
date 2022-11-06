### 通用接口测试工具

> 配置式的接口测试工具

## 快速开始

配置测试参数与期望
```json
{
  "title": "五角大楼-防撞测试",
  "baseUrl": "http://postman-echo.com",
  "meta": {
    "负责人": "拉倒"
  },
  "apis": [
    {
      "name": "echo post",
      "rout": "POST /post",
      "ext_valid": {},
      "cases": [
        {
          "param":{"json":{"name":"ladeng", "age":81, "l": 99}},
          "wants": {
            "http_code": 200,
            "resp": {
              "json.name": "ladeng",
              "json.age": [">", 18],
              "data.l": ["=", "$param.json.l"]
            }
          },
          "ext": []
        }
      ]
    }
  ]
}
```


