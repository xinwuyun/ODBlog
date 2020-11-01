from flask import Flask, render_template, redirect
from urllib import request
import blog
app = Flask(__name__)

@app.route('/')
def blogs():
    blogs = blog.get_blog_list()
    return render_template('blogs.html', blogs=blogs)

@app.route('/blog/<title>/')
def blog_content(title):
    content = blog.get_blog_content(name=title)
    return render_template('blog.html', content=content)

@app.route('/blog/<title>/<item>')
def show_item(title, item):
    link = blog.get_item(title, item)
    return redirect(link)

@app.route('/archives')
def archives():
    blogs = blog.get_blog_list()
    return render_template('archives.html', blogs=blogs)

@app.route('/categories/')
@app.route('/categories/<name>')
def categories(name=''):
    categories = blog.get_categories()
    cat_blogs = []
    if name:
        cat_blogs = categories[name]
    return render_template('categories.html', categories=categories, blogs=cat_blogs, name=name)

@app.route('/about')
def about():
    content = blog.get_about()
    return render_template('about.html', content=content)


@app.route('/admin')
@app.route('/admin/file/<path:path>')
def admin(path=''):
    blogs = blog.admin_get_list(path)
    return render_template('admin.html', blogs=blogs, path=path)