# -*- coding:utf-8 -*-
from flask import Flask, render_template, request
import recommend

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search/')
def search():
    # request为全局变量，可得到用户输入信息
    n = request.args.get('user')
    # 调用推荐函数
    dic = recommend.recommend(n)
    # 用返回的结果渲染模板
    return render_template('search.html', Data=dic)


if __name__ == '__main__':
    app.run(debug=True)
