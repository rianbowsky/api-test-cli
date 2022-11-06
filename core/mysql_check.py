#! python3

from .uitls import varParse,isWant

class MysqlCheck:

    def __init__(self, dbConn, sql, args, wants) -> None:
        self.dbConn = dbConn # 数据库链接
        # 参数存一份
        self.wants = wants
        self.sqlTpl = sql
        self.args = args
        self.context = {}

        self.tWants = {}  # 解析变量后的期望
        self.dbData = {}  # 从数据库查出的一条数据

        self.sql = '' # 实际执行的sql
        self.err = {} # 错误信息
    
    def sqlVarParse(self, context):
        '''sql变量转义'''
        param = {}
        for k in self.args:
            param[k] = varParse(self.args[k], context)
        self.sql = self.sqlTpl.format_map(param)

    def wantVarParse(self, context):
        '''解析期望中的变变量'''
        self.tWants = {}
        for k, want in self.wants.items():
            if not isinstance(want, list):
                self.tWants[k] =  varParse(want, context)
                continue
            if len(want) < 2:
                self.tWants[k] = want
                continue
            for i in range(1, len(want)):
                want[i] = varParse(want[i], context)
            self.tWants[k] = want 

    def fetchOne2Map(self):
        '''从数据库中查询一条数据'''
        with self.dbConn.cursor() as cur:
            cur.execute(self.sql)
            fieldIndex = {}
            i = 0
            for desc in cur.description:
                fieldIndex[desc[0]] = i
                i = i+1
            data = cur.fetchone()
            self.dbData = {}
            for i in fieldIndex:
                self.dbData[i] = data[fieldIndex[i]]
        return
    
    def iswant(self):
        '''期望对比'''
        self.err = {}
        self.wantVarParse(self.context)
        for k , want in self.tWants.items():
            if isWant(self.dbData[k], want):
                continue
            self.err[k] = {"field": k, "actual": self.dbData[k] ,"want": want}

    def check(self, context) -> bool:
        # 上下文信息存一份
        self.context = context
        # 生成真正执行的sql
        self.sqlVarParse(context)
        # sql查询,数据存到map中
        self.fetchOne2Map()
        # 生成真实期望
        self.wantVarParse(context)
        # 期望对比
        self.iswant()
        return len(self.err) == 0

    def logg(self):
        return {
            "succ": len(self.err) == 0,
            "sql": self.sql,
            "context": self.context,
            # "data": self.dbData,
            "unexpected": self.err
        }

if __name__ == '__main__':
    pass