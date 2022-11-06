
from typing import Dict
import json
class Report:
    '''报告数据模型
    '''
    def __init__(self) -> None:
        self.title = '接口测试报告'
        self.meta = {}
        self.apis = {} # 接口统计

    def setTitle(self, title:str) -> None:
        self.title = title

    def setMeta(self, meta:Dict)->None:
        self.meta = meta

    def addMeta(self, k:str, v:str) -> None:
        self.meta[k] = v

    def addApi(self, rout, name="", case=0, succ = 0, fail=0) -> None:
        self.apis[rout] = {
            "rout": rout,
            "name": name,
            "caseNum": case,
            "succNum": succ,
            "failNum": fail,
            "bugs": []
        }
    
    def addBug(self, rout, ex, context) -> None:
        if rout not in self.apis:
            self.addApi(rout)
        self.apis[rout]["bugs"].append({
            "unexpected": ex,
            "context": context
        })
        self.apis[rout]['failNum'] += 1

    def data(self) -> Dict:
        return {
            "title": self.title,
            "meta": self.meta,
            "apis": self.apis
        }

    def json(self) -> str:
        return json.dumps(self.data())