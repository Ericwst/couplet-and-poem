from flask import Flask, render_template, request, redirect, url_for, session
from flaskr.poem import nlp_result

app = Flask(__name__)

token_key = 'put your token here'


@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        couplets = request.form.get('couplets')
        if couplets is not None:
            return redirect(url_for('get_couplets'))
        poem = request.form.get('poem')
        if poem is not None:
            return redirect(url_for('get_poem'))

    return render_template('couplets/index.html')


@app.route("/couplets", methods=('GET', 'POST'))
def get_couplets():
    if request.method == 'POST':
        title = request.form.get('theme')
        back = request.form.get('back')
        if back == '返回':
            return redirect(url_for('index'))
        center, first, second = nlp_result(title, token_key, way='couplets')
        return render_template('couplets/show.html',
                               center=center,
                               first=first,
                               second=second,
                               title=title)
    return render_template('couplets/base.html')


@app.route("/poem", methods=('GET', 'POST'))
def get_poem():
    if request.method == 'POST':
        title = request.form.get('theme')
        back = request.form.get('back')
        if back == '返回':
            return redirect(url_for('index'))
        title, poem = nlp_result(title, token_key, way='poem')
        return render_template('couplets/poem_show.html',
                               title=title,
                               poem=poem)
    return render_template('couplets/poem_index.html')


if __name__ == '__main__':
    app.run(debug=True)
