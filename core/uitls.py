#! python3

def dataGet(data:map, field:str):
    '''map数据 深度获取
    '''
    keys = field.split('.')
    for k in keys:
        if k in data:
            data = data[k]
        else:
            return None
    return data

def varParse(var, context:map):
    '''变量转义

    变量为字符串,且为$开始,则尝试在上下文中获取该值
    '''
    if not isinstance(var, str):
        return var
    if var[0] != '$':
        return var
    return dataGet(context, var[1:])


opMap = {
    "=": lambda v1,v2: v1 == v2,
    ">": lambda v1,v2: v1 > v2,
    ">": lambda v1,v2: v1 > v2,
    "<": lambda v1,v2: v1 < v2,
    "<": lambda v1,v2: v1 < v2,
    "!=": lambda v1,v2: v1 != v2,
    "": False
}

def isWant(actual, want) -> bool:
    '''期望对比'''
    if not isinstance(want,list):
        return actual == want
    if len(want) == 0:
        return False
    if len(want) == 1:
        return actual == want[0]
    op, value = want
    return opMap[op](actual, value)

# 期望对比
def isWant2(actual, want, context={}) -> bool:
    if not isinstance(want,list):
        v = varParse(want, context)
        return actual == v
    if len(want) == 0:
        return False
    if len(want) == 1:
        v = varParse(want[0], context)
        return actual == v
    op, value = want
    v = varParse(value, context)
    return opMap[op](actual, v)
