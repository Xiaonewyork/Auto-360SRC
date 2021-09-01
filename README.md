# 前言

我们在使用通用漏洞刷SRC时，常常需要提交几十上百个目标，很容易把我们给累死。 于是我发明了这款360SRC自动填表脚本，它可以辅助我们填写重复的字段，同时还具有模板渲染功能，可以根据不同目标生成不同的内容，肥肠滴银杏。

# 使用步骤

## 环境配置
`pip install -r requirements.txt`  
然后配置selenium，我使用的是chrome浏览器，参考https://www.cnblogs.com/lfri/p/10542797.html  
修改`main.py`中webdriver的`executable_path`路径

## 简单使用
1. 首先登录[360SRC](https://src.360.net/) 
2. 然后将cookie填到`config.json`中的`cookies`字段
3. 根据附录的[关键字说明](#keywords)将想填写的内容填入到`template.json`中的`fields`对应的字段
4. 运行`main.py`

## 模板渲染
1. 在`template.json`中的`variables`中定义模板变量  
2. 然后在`fields`中的字段里使用`{{ 变量名 }}`引用  

ps：`url`是必需填的，并且如果没有定义`site_ip`变量，则会根据`url`获取站点ip并赋给`site_ip`。也就是说至少有`url`和`site_ip`两个模板变量。

# 附录

## 关键字说明<div id="keywords"></div>

| 关键字 |对应字段 |
| :----: |:----: |
| repair | 修复方案 |
| info | 漏洞简介 |
| steps | 复现步骤 |
| company | 归属厂商 |
| title | 漏洞标题 |
| component | 通用漏洞组件 |
| url | 漏洞url |
| site_title | 站点标题 |
| site_ip | 站点ip |

若违规联系本人删除。
