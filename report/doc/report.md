# {{title}}

{% for k,v in meta.items() %}
> {{k}}: {{v}}  {% endfor %}
## 总览

执行用例:`{{totalCase}}` 成功:`{{totalCase - failNum}}` 失败:`{{failNum}}`

| 接口名称| 路由 | 用例数 | 成功| 失败 |
| -------| ----| ----- | ---| ---- |{% for a in apis.values() %}
| {{a.name}} | {{a.rout}} | {{a.caseNum}}| {{a.caseNum - a.failNum}} | {{a.failNum}} |{% endfor %}

---
{% if failNum != 0 %}
## bug详情
{% endif %}{% for a in apis.values() %}{% for bug in a.bugs %}
#### {{bug.name or a.rout}}
- 接口地址: `{{a.rout}}`  
- 上下文:  
```json
{{bug.context}}
```

- 差异:  
  {% for e in bug.unexpected %}  [{{e.tag}}] 字段 `{{e.field}}` 期望值 `{{e.want}}` 实际值: `{{e.actual}}`  
{% endfor %}{% endfor %}{% endfor %}
