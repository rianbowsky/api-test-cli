#! python3

import argparse
from http.client import OK
import json
from report.md import outMd

from report.model import Report
from core.http_api import HttpApi

# 入参, case-xxx.json 和 case-xxx-secret.json

# 用例
cases = {}
# secret配置
conf = {}

parser = argparse.ArgumentParser(description="api-teeeeeeest")
parser.add_argument('-c', '--case', help='测试用例配置文件(json)',)
parser.add_argument('-s', '--secret', help='其他私密配置')
parser.add_argument('-o', '--out', help='测试报告文件位置', default='./report.md')
args = parser.parse_args()

print(args, args.case)

def paramParse():
    if args.case == None:
        print("[参数错误] 未指定case.json")
        parser.print_usage()
        exit(0)
    # 解析 case 配置 写入全局变量
    global cases, conf
    with open(args.case,'r', encoding='utf-8') as fp:
       cases = json.load(fp)
    if args.secret != None:
        with open(args.secret,'r', encoding='utf-8') as fp:
            conf = json.load(fp)

def main():
    # 参数解析
    paramParse()
    r = Report()
    r.setTitle(cases['title'])
    baseUrl = cases['baseUrl']
    r.setMeta(cases['meta'])
    for a in cases['apis']:
        api = HttpApi(baseUrl, a['rout'],headers={})
        r.addApi(a['rout'], a['name'] or '-', len(a['cases']))
        for c in a['cases']:
            assert c['wants'] != None
            ok = api.Check(c['param'], c['wants'])
            if not ok:
                # 记录bug
                r.addBug(a['rout'],list(api.err.values()), api.context())
            
    outMd(args.out, r.data())


if __name__ == '__main__':
    main()

print(cases)
print(conf)