# 数据库相关
import os
import sys
import click

# flask框架
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy # 导入扩展
from flask import request,url_for,redirect, flash

# 相当于java中创建对象
app = Flask(__name__)
# 配置数据库的路径, 相当于java项目中的配置文件
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(app.root_path, 'data.db')
# 关闭对模型修改的监控
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 设置密钥
app.config['SECRET_KEY'] = 'dev'
# 初始化扩展, 传入程序实例app
db = SQLAlchemy(app)


# 创建数据库模型, 继承db.Model
class User(db.Model):
    # 约束为主键, 类型int
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


# 自定义命令
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database') # 输出提示信息

# 自定义导入数据命令
@app.cli.command()
def forge():
    db.drop_all()
    db.create_all()
    # 定义虚拟数据
    name = 'Test'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

#     创建对象
    user = User(name=name)
    # 添加至数据库
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    # 提交命令
    db.session.commit()
    click.echo("Done")


# 注册首页处理函数
@app.route("/",methods=['POST','GET'])
def index():
    # 渲染, 左边是模版中的变量, 右边是指向的实际对象
    # return render_template('index.html',name=name,movies=movies)
    # user = User.query.first()

    if request.method == 'POST': # 判断请求的方式
        # 获取表单数据
        title = request.form.get('title')# 根据表单中的name属性获取值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) >4 or len(title) >60:
            # 重定向到首页
            flash("Invalid input")
            return redirect(url_for('index'))
        # 保存到数据库
        movie = Movie(title=title,year=year)
        db.session.add(movie)
        db.session.commit()
        flash("添加成功")
        return redirect(url_for('index'))

    movies = Movie.query.all()
    return render_template('index.html',movies=movies)

# 注册错误处理函数
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# 模版上下文处理函数, 模版公用的数据
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user) #返回字典, 等同于return {'user':user}


# add添加操作
@app.route('/add', methods=['post'])
def add():
    # if request.method == 'POST': # 判断请求的方式
    # 获取表单数据
    title = request.form.get('title')# 根据表单中的name属性获取值
    year = request.form.get('year')
    # 验证数据
    if not title or not year or len(year) >4 or len(title) >60:
        # 重定向到首页
        flash("Invalid input")
        return redirect(url_for('index'))
    # 保存到数据库
    movie = Movie(title=title,year=year)
    db.session.add(movie)
    db.session.commit()
    flash("添加成功")
    return redirect(url_for('index'))

# 编辑操作
@app.route('/movie/edit/<int:movie_id>', methods=['POST','GET'])
def edit(movie_id):
    # 如果是get请求, 获取电影的修改前信息
    movie = Movie.query.get_or_404(movie_id)
    # 如果是post请求, 获取修改后的数据, 保存到数据库, 并返回主页
    if request.method == 'POST':
        movie.title = request.form['title']
        movie.year = request.form['year']
        db.session.commit()
        flash('Item update')
    #     重定向
        return redirect(url_for('index'))
    return render_template('edit.html',movie=movie)

@app.route('/movie/delect/<int:movie_id>',methods=['GET'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("Item deleted")
    return redirect(url_for('index'))