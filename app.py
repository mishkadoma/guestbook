from flask import Flask, redirect, render_template, url_for, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/view')
def view():
    return render_template('view.html')

@app.route('/posts', methods=['POST'])
def posts():
    name = request.form['name']
    post = request.form['post']
    return render_template('view.html', name=name, post=post)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
