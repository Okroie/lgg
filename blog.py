# *_* coding: UTF-8 *_*
# Team: BigData Two
# Time: 2022/7/19 10:14
# Name: Okroie
# Program: blog.PY
# Format: PyCharm

from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'scd dsd ds dd, 666'


def get_db_conn():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_conn()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    return post


@app.route('/')
def index():
    # return 'Hello Flask'
    conn = get_db_conn()
    posts = conn.execute('SELECT * FROM posts ORDER BY created desc').fetchall()
    return render_template('index.html', posts=posts)


@app.route('/posts/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/posts/new/', methods=('GET', 'POST'))
def new():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('标题不能为空')
        elif not content:
            flash('内容不能为空')
        else:
            conn = get_db_conn()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
            flash('文章保存成功！')
            return redirect(url_for('index'))
    return render_template('new.html')


@app.route('/posts/<int:post_id>/edit', methods=('GET', 'POST'))
def edit(post_id):
    post = get_post(post_id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('标题不能为空')
        else:
            conn = get_db_conn()
            conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, post_id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('edit.html', post=post)


@app.route('/posts/<int:post_id>/delete', methods=('POST',))
def delete(post_id):
    post = get_post(post_id)
    conn = get_db_conn()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    flash('"{}" 删除成功'.format(post['title']))
    return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html', movie='static/movies/kb.mp4')


if __name__ == '__main__':
    app.run(debug=True)
