#! python3
import requests
from .uitls import dataGet,isWant, varParse

class HttpApi:
    tag = '响应'
    def __init__(self, baseUrl:str, rout:str, headers:map) -> None:
        self.baseUrl = baseUrl
        self.headers = headers
        [method, path] = rout.split(' ', maxsplit=2)
        self.method = method.lower()
        self.path = path
        self.url = self.baseUrl.rstrip('/') + '/'+ self.path.lstrip('/')
        # 存响应数据
        self.params = None
        self.resp = None
        self.err = {}
    
    def fetchResp(self, params:map):
        '''获取响应'''
        self.params = params
        resp = requests.request(self.method, self.url, headers= self.headers,
            json = params['json'] if 'json' in params else None ,
            params = params['params'] if 'params' in params else None,
            data = params['data'] if 'data' in params else None
        )
        self.resp = resp
        return resp

    def addErr(self, k:str, actual, want, tag=""):
        self.err[k] = {
            'tag': tag or self.tag,
            'field': k,
            'actual': actual,
            'want': want, 
        }

    def isWant(self, wants:map):
        '''期望对比逻辑
        '''
        self.err = {}
        if 'http_code' in wants:
            if not isWant(self.resp.status_code, wants['http_code']):
                # 如果状态码都错误,就没必要对比响应了
                self.addErr('http_code', self.resp.status_code, wants['http_code'], tag="状态码")
                return
        if 'resp' in wants:
            # resp 的期望支持请求中的变量
            wants['resp'] = self.wantParse(wants['resp'],{
                "param": self.params,
            })
            data = self.respParseJson()
            for k, v in wants['resp'].items():
                actual = dataGet(data, k)
                if isWant(actual, v):
                    continue
                # 记录错误
                self.addErr(k, actual, v, tag='响应体')
    def wantParse(self, wants, context):
        ret = {}
        for k, want in wants.items():
            if not isinstance(want, list):
                ret[k] = varParse(want, context)
                continue
            if len(want) == 1:
                ret[k] = varParse(want[0], context)
                continue
            for i in range(1, len(want)):
                want[i] = varParse(want[i], context)
            ret[k] = want
        return ret
    
    def respParseJson(self):
        json = {}
        try:
            json = self.resp.json()
        except:
            pass
        return json
    
    def Check(self, param,  wants)->bool:
        # 请求接口
        self.fetchResp(param)
        # 期望对比
        self.isWant(wants)
        return len(self.err) == 0
        
    def context(self):
        return {
            "rout": "%s %s"% (self.method, self.url),
            "param": self.params,
            "http_code": self.resp.status_code,
            "resp": self.respParseJson(),
        }

if __name__ == '__main__':
    db_valid = [
        {
            "udf_name": "recordHas",
            "sql": "select count(*) as num from bs_users where phone={phone}",
            "args": {
                "phone": "$param.json.phone"
            },
            "wants": {
                "num": 1
            }
        },
        {
            "udf_name": "fieldCp",
            "sql": "select * from bs_users where phone={phone}",
            "args": {
                "phone": "$param.json.phone"
            },
            "wants": {
            }
        }
    ]
    rout = "POST /v1/user/regist"
    case = {
        "param": {
            "json": {
                "phone":"18681636749",
                "code": "123456"
            }
        },
        "wants": {
            "http_code": 200,
            "resp": {
                "errCode": 0,
            },
        },
        "db_check": ["recordHas", "fieldCp"]
    }
    baseUrl = "http://127.0.0.1:8081"
    api = HttpApi(baseUrl, rout, {})
    resp = api.fetchResp(case["param"])
    print(resp.status_code)