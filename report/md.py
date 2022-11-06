#! python3
import json
import os
from jinja2 import Environment, FileSystemLoader

templDir = os.path.join(os.path.dirname(__file__), 'doc')
env = Environment(loader=FileSystemLoader(templDir))

def outMd(file, data):
    '''输出报告
    '''
    fp = open(file, mode='w', encoding='utf-8')
    # 计算总览
    data["totalCase"] = listSum(data["apis"].values(), 'caseNum')
    data['failNum'] = listSum(data["apis"].values(), 'failNum')
    for a in data['apis'].values():
        for bug in a['bugs']:
            bug['context'] = json.dumps(bug['context'],indent=2)
    h = env.get_template('report.md')
    out = h.render(data)
    fp.write(out)
    fp.flush()
    fp.close()

def listSum(l:dict[dict], key) ->int:
    sum = 0
    for v in l:
        sum += v[key]
    return sum

if __name__ == '__main__':
    pass