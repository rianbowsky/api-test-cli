#! python3

import init

from report.model import Report
r = Report()
r.setTitle('最后一课,zzzzz')
r.setMeta({
    "地址": "http://127.0.0.1:8089/996",
    "责任人": "张三",
    "时间": "2022-10-11"
})
r.addApi('post a/b/c', case=5)
r.addBug(
    'post a/b/c',
    [
        {'tag': '响应码', 'key':'http_code', 'want':'200', 'got':400}
    ],
    {
        "param":{},
        "resp":{"retCode": 0, "msg": "succ"},
        "http_code": 400,
    }
)
print(r.json())