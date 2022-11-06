#! python3
import init

from core.http_api import HttpApi
from report.md import outMd
from report.model import Report

baseUrl = "http://postman-echo.com"
rout = "POST /post"
case = {
    "param": {
        "json":{
            "name":"lilei",
            "age":18
        }
    },
    "wants": {
        "http_code": 200,
        "resp": {
            "json.name": "lilei",
            "data.age": ['<', 10]
        }
    }
}

r = Report()
r.setTitle("测试的测试报告")
r.setMeta({
    "地址": baseUrl,
})
r.addApi(rout, "echo POST", 2)
api = HttpApi(baseUrl, rout, {})
ok = api.Check(case["param"], case["wants"])
if not ok:
    r.addBug(rout, list(api.err.values()), api.context())
# print(r.data())
outMd("./out/ce.md", r.data())
