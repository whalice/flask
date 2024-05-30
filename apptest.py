# 从flask包引入Flask类
from flask import Flask
from markupsafe import escape
from flask import url_for

# 实例化, 创建对象app
app = Flask(__name__)

# 注册一个函数, 处理请求, 使用route()装饰器绑定url
# url映射的请求处理函数
# 绑定多个url规则
@app.route("/index")
@app.route("/")
def index():
    return "hello world"

# 返回html元素内容, 龙猫的动图
@app.route("/hello")
def hello():
    return '<img src="http://helloflask.com/totoro.gif">'

# 定义变量
@app.route("/user/<name>")
def name(name):
    # 对变量进行转义处理
    return f'User:{escape(name)}'

@app.route("/test")
def test1():
    print(url_for('hello'))
    print(url_for('test1',num=2))
    print(url_for("name",name='test'))
    return '222'


