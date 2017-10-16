from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
import database_entry


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_entry.database_credentials
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    comment = db.Column(db.String(2000))


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

    signature = Posts(name=name, comment=post)
    db.session.add(signature)
    db.session.commit()

    result = Posts.query.all()
    return render_template('view.html', result=result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
